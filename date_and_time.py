"""
Author          :   Or Israeli
FileName        :   date_and_time.py
Date            :   13.11.17
Version         :   1.0
Description     :   A program that checks the current date, day
                    time and weather and delivers the data to the gui screen.
"""
from datetime import datetime
from constants import *
import urllib2
import json
import pyowm


class DateAndTime(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def get_date():
        """

        The function checks what date is today and returns today's date.

        Returns:
            string: The date of today.

        """
        now = datetime.now()
        year = str(now.year)
        month = str(now.month)
        day = str(now.day)
        return "/".join([day, month, year])

    @staticmethod
    def get_day():
        """

        The function checks what day is today and returns today's day.

        Returns:
            string: The day of today.

        """
        return WEEK_DAYS_DICT[datetime.today().weekday()]

    @staticmethod
    def check_weather():
        """

        The function checks the current outside weather and returns
        the weather right now.

        Returns:
            string: The outside weather right now.

        """
        owm = pyowm.OWM(WEATHER_API)
        observation = owm.weather_at_place(DateAndTime.get_place())
        weather = observation.get_weather()
        return weather

    @staticmethod
    def get_temperature():
        """

        The function extracts the temperature from the weather
        and returns the temperature right now.

        Returns:
            string: The outside temperature right now.

        """
        weather = DateAndTime.check_weather()
        temperature = weather.get_temperature(CELSIUS)
        current_temperature = str(int(temperature[CURRENT_TEMP]))
        return current_temperature

    @staticmethod
    def get_weather_status():
        """

        The function extracts the weather status from the weather
        and returns the weather status right now.

        Returns:
            string: The outside weather status right now.

        """
        weather = DateAndTime.check_weather()
        status = repr(weather).split(STATUS)[1][:-1]
        if MORNING < datetime.now().hour < EVENING:
            part_of_day = DAY
        else:
            part_of_day = NIGHT
        return status, part_of_day

    @staticmethod
    def get_place():
        """

        The function checks where we are now and returns
        our current location by country and city.

        Returns:
            string: Our current location.

        """
        f = urllib2.urlopen(JSON_URL)
        json_string = f.read()
        f.close()
        location = json.loads(json_string)
        country = location[COUNTRY_CODE]
        city = location[CITY_CODE]
        return ", ".join([city, country])
