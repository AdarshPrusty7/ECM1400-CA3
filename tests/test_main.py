import pytest
from main import get_notifications, weather_handler, get_weather, news_handler, get_news, \
    covid_handler, get_covid

"""
The modules to test are as such:
get_notifications - see if it returns a list
weather_handler - see if it returns 4 variables: float, int, int, string
get_weather - see if it returns a dictionary
news_handler - see if it returns a dictionary
get_news - see if it returns a list
covid_handler - see if it returns a dictionary
get_covid - see if it returns a dictionary

I can only test these modules because the others don't return anything. I can only test their return
 values for types because the data is fluid.
"""


def test_get_notifications():
    assert (isinstance(get_notifications(True, True), list) == True)
    assert (isinstance(get_notifications(False, False), list) == True)
    assert (isinstance(get_notifications(True, False), list) == True)
    assert (isinstance(get_notifications(False, True), list) == True)


def test_weather_handler():
    assert (isinstance(weather_handler(), (float, int, int, str)) == True)


def test_get_weather():
    assert (isinstance(get_weather(), dict) == True)


def test_news_handler():
    assert (isinstance(news_handler(), dict) == True)


def test_get_news():
    assert (isinstance(get_news(), list) == True)


def test_covid_handler():
    assert (isinstance(covid_handler(), dict) == True)


def test_get_covid():
    assert (isinstance(get_covid(), dict) == True)


def main_test():
    test_get_notifications()
    test_weather_handler()
    test_get_weather()
    test_news_handler()
    test_get_news()
    test_covid_handler()
    test_get_covid()


main_test()
