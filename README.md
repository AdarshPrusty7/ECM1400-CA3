# ECM1400 Smart Alarm

This is a smart alarm programmed for ECM1400's Continuous Assessment 3. This code can be found on
https://github.com/AdarshPrusty7/ECM1400-CA3. As of this submission, it is a private repo, but will
(hopefully) be public by the time you receive this project.

## Introduction
This is a basic smart alarm. One can set alarms and receive notifications. Every hour, the user
 will receive a text-based notification including covid19 stats, a weather briefing, and news
  headlines. 
  
A user can set their alarm for whenever they want, however, alarms set in the past
will not run and alarms set beyond the year 9999 will not be registered at all. The user can
specify, when they set their alarm, whether they'd like to receive a news and/ or weather
briefing alongside it. Covid19 stats will always be displayed. 
     
Multiple alarms of the same label are not allowed. If it is attempted, the second alarm will not
 be registered at all. The program is designed to catch this.

A log file can be viewed at `pysys.log`, and a config file at `config.json`.

## Prerequisites

- Python 3.8+
- Weather API key from https://openweathermap.org/api
- News API key from https://newsapi.org/
- A stable internet connection
- Latest Version of `pip`

## Installation

- **pyttsx3 -** `pip install pyttsx3`
- **requests -**  `pip install requests`
- **flask -** `pip install Flask`
- **newsapi -** `pip install newsapi-python`
- **uk-covid19 -** `pip install uk-covid19`

## Changing Config
The `config.json` file provided can and should be edited by the user. One must insert their
 respective API keys under the `"API-keys"` as indicated, for weather and news updates.
 Ensure the API-key only is in quotes, as such, "123456789", not "<123456789>".
 
 Additionally, under the `"settings"` section, one can alter various options. 
 
 One can alter the city whose weather data one wants to read. This is currently set to `"London
 "` in `"weather_city"`. 
 
 One can alter the **minute** on which notifications are sent every hour (e.g. if set to `"47
 "`, notifications will be sent at `12:47`, `13:47`,` 14:47`, etc.) in `"notification_time"`.
 
 One can alter the news sources they get their news notifications from. They can be viewed here
  (https://newsapi.org/docs/endpoints/sources). When doing so, care must be taken to include the
   additional source **inside** the quotation marks. For example, `"news_sources` is currently
    set to `"bbc-news"`. If one wished to add 'the verge' as a source, they would need to replace
     `"bbc-news"` with `"bbc-news, the-verge"`.
     
One can alter the number of articles they receive per news notification request. `"article_number
"` is currently set to `3`. Although this number can be raised, if the number of articles is set
 to a number higher than 10, the program will default to a set value of 5 articles.
 
One can alter the structure of the Covid19 data they receive in their notifications. It is not
 recommended you do this, unless you've looked at the module's documentation yourself.
 
 ## Using The Alarm Clock
 #### Alarm
 To add an alarm, you simply enter in a date and time in the format as shown in the form. Note that 
 the form will not accept any date beyond the year 9999 as an alarm date. Alarms set in the past 
 will not trigger, but will still appear on the left-hand side. You must cancel them manually to get
  rid of them.
 
 The user may choose to include a news and/or weather notification briefing as their alarm is set 
 off. This can be chosen when they first make their alarm, and is indicated by the check boxes.
 
 To remove an alarm, simply click on the cross mark on the alarm's tab header.
 
 #### Notifications
 Notifications are sent every hour, at the minute of the user's choosing. By default, it is set to 
 to send at every '00', but this can be changed in the config file provided. See the 'Changing Config'
 section for more information on this.
 
 When the user is sent a non-alarm notification, they will be unable to delete them for under a minute. 
 Otherwise, they will be able to delete the notification immediately.  

## Testing
Errors occurred on the development side when pylint was used, so basic assertion error tests were 
used. These were compiled into one function which can be executed in the tests folder in
`test_main.py`.
 
 
 
## Known Issues
**These are some issues that I couldn't iron out by the final version of this project.**

- When submitting an alarm, double clicking on the button will result in an internal server error
. Simply navigate back to '/' or 'index' or press the 'back' button on your browser and resubmit
 your form (don't double click this time).
- On occasion, after an alarm has been triggered, the alarm notification on the left-hand side
  will not go away. You must manually remove it in this case, by clicking on the cross mark on
   its tab header.
- If you schedule an alarm for the next minute (e.g. set at `12:46` for `12:47`), the alarm
 notification won't pop up until the actual alarm has been triggered. You will then have to
  manually remove the alarm.
- Alarms set in the past will not trigger but they will show up on left-hand side. You can get
 rid of these by click on the cross mark on its tab header.
- Once a normal notification (i.e. not a notification sent off by an alarm) has been sent, you
 will not be able to delete for under a minute after it is sent, depending on when the page next
  refreshes itself.
- If in doubt, refresh the page.


## Details

#### Author(s): Adarsh Prusty

#### MIT License

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

#### Link to Source

This code can be found on
https://github.com/AdarshPrusty7/ECM1400-CA3. 
