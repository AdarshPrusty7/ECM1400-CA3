
"""
This is a smart alarm clock for ECM1400's Continuous Assessment 3
"""

# Imports initialised
import datetime
import json
import logging
import sched
import time

import pyttsx3
import requests
from flask import Flask, request, render_template, Markup
from newsapi import NewsApiClient
from uk_covid19 import Cov19API

LOGGING_FORMAT = '%(levelname)s: [%(asctime)s] -- %(message)s'
logging.basicConfig(filename="pysys.log", level=logging.DEBUG, format=LOGGING_FORMAT)

# API keys, settings and the structure of the Covid19 notifications are initialised
logging.info("opening config file")
with open('config.json', 'r') as f:
    json_file = json.load(f)
keys = json_file["API-keys"]
logging.info("keys loaded from config file")
settings = json_file["settings"]
logging.info("settings loaded from config file")
covidstructure = json_file["cases_and_deaths"]
logging.info("covidstructure loaded from config file")

england_only = [
    'areaType=nation',
    'areaName=England'
]

logging.info("scheduler initialising")
s = sched.scheduler(time.time, time.sleep)  # Sets up alarm scheduler
logging.info("scheduler initialised")
# Below set site logo and favicon
IMAGE = 'alarmSymbol.png'
FAVICON = 'alarmSymbol.ico'

alarms = []  # The list that's returned to the HTML template for alarms
notifications = []  # The list that's returned to the HTML template for notifications
logging.info("alarms and notifications lists initialised")
NOTIFICATION_TIME = settings["notification_time"]  # The minute at which regular notifs are sent
NEWS_ARTICLE_NUMBER = settings["article_number"]  # Number of articles in news briefing
NEWS_SOURCES = settings["news_sources"]  # Sources for news
logging.info("covid settings initialised")

if NEWS_ARTICLE_NUMBER > 10:  # Error checking to ensure too many articles aren't sent
    NEWS_ARTICLE_NUMBER = 5
# The below if statement checks if the user inputted a double digit value
if not NOTIFICATION_TIME.isnumeric() or len(NOTIFICATION_TIME) != 2:
    NOTIFICATION_TIME = "00"
logging.info("covid settings checked")

# Creates weather API URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
weather_api = keys["weather"]
news_api_key = keys["news"]
city_name = settings["weather_city"]

complete_weather_url = BASE_URL + "appid=" + weather_api + "&q=" + city_name
logging.info("weather api initialised")

# Extracts news API key
complete_news_api = NewsApiClient(api_key=news_api_key)
logging.info("news api initialised")

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def main():
    """This module is the central hub for this program.
    Because of the way I started building it, I was unable to isolate various features into
    separate modules. This includes the sections that adds alarms, deletes alarms and deletes
    notifications.
    """

    # Gets args used in form submission on site
    alarm = request.args.get('alarm')
    name = request.args.get('two')
    alarm_item = request.args.get('alarm_item')
    notif_item = request.args.get('notif')
    news_item = request.args.get('news')
    weather_item = request.args.get('weather')

    time_right_now = datetime.datetime.now()  # Gets current datetime object

    if str(time_right_now)[14:16] == str(NOTIFICATION_TIME):  # Checks if time matches what user set
        get_notifications(True, True)  # Default notifs will send out weather and news
        logging.info("notifications added")

    if alarm:  # If new alarm has been requested
        logging.info("alarm creation requested")
        if not alarm[0:5].isnumeric():  # Checks if year is > 9999
            logging.info("alarm year <= 9999 confirmed")
            formatted_datetime = datetime.datetime(int(alarm[0:4]), int(alarm[5:7]),
                                                   int(alarm[8:10]),
                                                   int(alarm[11:13]), int(alarm[14:16]))
            # Above converts requested time into datetime object
            difference = formatted_datetime - time_right_now
            difference_seconds = difference.days * 86400 + difference.seconds
            # Converts difference into seconds only

            corrdict = (next((item for item in alarms if item["title"] == name), None))
            # corrdict is a True, None statement
            # It looks through the alarms list, and tries to find a title with same value as 'name'
            if not corrdict:  # Triggers if an alarm with the same label as 'name' doesn't exist
                logging.info("new alarm being added")
                event = s.enter(difference_seconds, 1, tts_request, (name,))  # Event is entered
                alarms.append(
                    {"title": name, "content": str(formatted_datetime) + "\n", "event": event})
                logging.info("new alarm added")
                # event is appended to alarms list (which is then passed to html template)
                if news_item:  # If check box was ticked
                    alarms[-1]["news"] = True  # Assign True to news key
                    logging.info("news = True added to alarm")
                else:
                    alarms[-1]["news"] = False  # Otherwise assign False
                    logging.info("news = False added to alarm")
                if weather_item:
                    alarms[-1]["weather"] = True  # See news
                    logging.info("weather = True added to alarm")
                else:
                    alarms[-1]["weather"] = False
                    logging.info("weather = False added to alarm")

        render_template('index.html', title='ECM1400 Alarm', alarms=alarms,
                        notifications=notifications, image=IMAGE,
                        favicon=FAVICON)  # In theory, refreshes page

    if alarm_item:  # If alarm deleted
        logging.info("alarm being deleted")
        for counter, item in enumerate(alarms):
            if item["title"] == alarm_item:  # Finds alarm in alarms
                s.cancel(alarms[counter]["event"])  # Cancel alarm in alarms
                logging.info("alarm cancelled")
                del alarms[counter]  # Deletes alarm entry in alarms
                logging.info("alarm entry removed from alarms")

    if notif_item:  # If notification deleted
        logging.info("notification being deleted")
        for counter, item in enumerate(notifications):
            if item["title"] == notif_item:  # Finds notification in notifications
                del notifications[counter]  # Delete notification entry from notifications

    render_template('index.html', title='ECM1400 Alarm', alarms=alarms, notifications=notifications,
                    image=IMAGE,
                    favicon=FAVICON)  # In theory, refreshes page
    get_time()  # Constantly checks for time, runs alarm if it should run within a minute
    cleanup()  # Cleans up any discrepancies between alarms and scheduler queue

    return render_template('index.html', title='ECM1400 Alarm', alarms=alarms,
                           notifications=notifications, image=IMAGE,
                           favicon=FAVICON)  # Returns page


@app.route('/tts_request')
def tts_request(announcement="Text to speech example announcement!"):
    """Typical text to speech module."""
    engine = pyttsx3.init()  # Engine initialised
    engine.say(announcement)  # Announcement spoken
    logging.info("tts engaged")
    engine.runAndWait()
    return "Hello text-to-speech example"


####################################################################################################
@app.route('/get_time')
def get_time():
    """This module checks if any alarm is within one minute of the time it should run."""
    right_now = datetime.datetime.now()  # Gets current datetime object
    for counter, item in enumerate(alarms):
        formatted_datetime = datetime.datetime(int(item["content"][0:4]), int(item["content"][5:7]),
                                               int(item["content"][8:10]),
                                               int(item["content"][11:13]),
                                               int(item["content"][14:16]))
        difference = formatted_datetime - right_now
        # Above Calculates difference between now and each alarm running
        difference_seconds = difference.days * 86400 + difference.seconds
        if 60 > difference_seconds >= 0:
            logging.info("scheduler to run")
            # If the alarm hasn't passed, and is within one minute of running, run
            get_notifications(alarms[counter]["weather"], alarms[counter]["news"])
            #  Unlike before, this get_notification's weather & news output is dependant on checkbox
            del alarms[counter]  # Deletes alarm from alarms
            s.run()  # Runs scheduler
            logging.info("alarm sent")
            cleanup()  # Should clean up any discrepancies
            render_template('index.html', title='ECM1400 Alarm', alarms=alarms,
                            notifications=notifications,
                            image=IMAGE, favicon=FAVICON)  # In theory, should refresh page
            return main()


@app.route('/cleanup')
def cleanup():
    """This module cleans up any discrepancies between alarms and scheduler queue."""
    for counter, item in enumerate(alarms):
        if item["event"] not in s.queue:  # Checks if alarm event is not in queue
            del alarms[counter]  # If so, delete alarm
            logging.info("alarm cleaned up")
    return "cleaned up"


####################################################################################################
@app.route('/get_notifications')
def get_notifications(weather_item, news_item):
    final_notification = []  # Final notification (F_N) to be returned
    covid_notification = get_covid()  # Responds with dictionary notification for Covid
    final_notification.append(covid_notification)  # Appends covid_notification to F_N
    logging.info("covid notification added")
    if weather_item:  # If checkbox was ticked
        weather_notification = get_weather()  # Responds with dictionary notification for weather
        final_notification.append(weather_notification)  # Appends weather_notification to F_N
        logging.info("weather notification added")
    if news_item:  # If checkbox was ticked
        news_notification = get_news()  # Responds with list of dictionaries for news
        for _, article in enumerate(news_notification):  # For each dict in the list
            final_notification.append(article)  # Append each news article as a separate notif
        logging.info("news notification added")

    global notifications  # Use the global variable, instead of a local variable
    notifications = final_notification  # Previous notifications are reset

    return "notifications gotten"


@app.route('/weather_handler')
def weather_handler():
    """This module uses the Weather API to grab weather data for a notification"""
    weather_json = requests.get(complete_weather_url).json()  # Get data and turn into json file
    logging.info("weather_json retrieved")
    if weather_json["cod"] != "404":  # If weather could be found
        main_stats = weather_json["main"]
        current_temperature = main_stats["temp"]
        current_pressure = main_stats["pressure"]
        current_humidity = main_stats["humidity"]
        main_weather = weather_json["weather"]
        weather_description = main_weather[0]["description"]
        # The above just extracts stats required for a notification
        return current_temperature, current_pressure, current_humidity, weather_description
    else:  # Because this function is called by another, it should return something
        return None, None, None, None


@app.route('/get_weather')
def get_weather():
    """This module sends off a weather notification"""
    current_temperature, current_pressure, current_humidity, weather_description = weather_handler()
    weather_notification = Markup("Temperature (degrees Celsius) = " + str(
        round(current_temperature - 273, 2)) + ",<br/>Atmospheric Pressure (hPA) = " + str(
        current_pressure) + ",<br/>Humidity (Percentage) = " + str(
        current_humidity) + ",<br/>Description: " + str(
        weather_description))
    # Above formats the weather notification
    return {"title": "Weather Report", "content": weather_notification}


@app.route('/news_handler')
def news_handler():
    """This module grabs the news data using the news api"""
    top_headlines = complete_news_api.get_top_headlines(sources=NEWS_SOURCES, language='en')
    logging.info("top_headlines retrieved")
    # Uses source 'NEWS_SOURCE' as specified in config file
    return top_headlines


@app.route('/get_news')
def get_news():
    """This module sends off a (couple of) news notification(s)"""
    headlines = []  # initialises headline list for dictionaries
    top_headlines = news_handler()
    for counter in range(NEWS_ARTICLE_NUMBER):
        headlines.append({"title": top_headlines["articles"][counter]["title"],
                          "content": top_headlines["articles"][counter]["description"]})
        # Above adds each article to headlines list as a separate notification
    return headlines


@app.route('/covid_handler')
def covid_handler():
    """This module grabs covid data from a module"""
    # covidstructure is specified in config file
    api = Cov19API(filters=england_only, structure=covidstructure)
    covid_data = api.get_json()  # Gets a json file of covid data
    logging.info("covid_data retrieved")
    return covid_data["data"][0]  # Gets the latest day's data


@app.route('/get_covid')
def get_covid():
    """This module sends off a covid notification. You can't get covid from this."""
    covid_data = covid_handler()
    covid_content = Markup("Date: " + str(covid_data["date"]) + ",<br/>Country: " + str(
        covid_data["areaName"]) + ",<br/>New Cases: " + str(
        covid_data["newCasesByPublishDate"]) + ",<br/>Total Cases: " + str(
        covid_data["cumCasesByPublishDate"]))
    # The above formats the covid data, ready to send it off as a notification
    covid_notification = {"title": "Covid Cases", "content": covid_content}
    return covid_notification


if __name__ == '__main__':
    app.run()

"""
MIT License

Copyright (c) 2020 Adarsh Prusty

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""