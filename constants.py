import os
import ipgetter

MY_IP = ipgetter.myip()
FOLDER_NAME = "c-o-s folder"
SYSTEM_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), FOLDER_NAME)
FILE_LIST_DIRECTORY = 1
BUFFER = 1024
FILE_ADDED_ACTION = "1"
FILE_DELETED_ACTION = "2"
FILE_MODIFIED_ACTION = "3"
READING = "rb"
WRITING = "wb"
FILE_BUFFER = 300000

CLOUD_HOST = "0.0.0.0"
CLOUD_IP = "127.0.0.1"
CLOUD_PORT = 8820
NUMBER_OF_CLIENTS = 1
CLOUD = "cloud"
CLOUD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), CLOUD)

SEPARATOR = "#"

WEEK_DAYS_DICT = {6: "Sunday", 0: "Monday", 1: "Tuesday",
                  2: "Wednesday", 3: "Thursday",
                  4: "Friday", 5: "Saturday"}

WEATHER_DAY_STATUS = {"Clear": "sun_day.jpg", "Rain": "rain_day.jpg", "Clouds": "cloud_day.jpg"}
WEATHER_NIGHT_STATUS = {"Clear": "sun_night.jpg", "Rain": "rain_night.jpg", "Clouds": "cloud_night.jpg"}

SPACES = " "*21
SPACESS = " "*28
DOWNLINES = "\n"*5

JSON_URL = 'http://freegeoip.net/json/'
COUNTRY_CODE = "country_code"
CITY_CODE = "city"
WEATHER_API = "da364b70e98bf854ba4c00c0c509eaf8"
STATUS = "status="
CELSIUS = "celsius"
CELSIUS_SIGN = " C"
CURRENT_TEMP = "temp"

MORNING = 6
EVENING = 17
DAY = "DAY"
NIGHT = "NIGHT"
