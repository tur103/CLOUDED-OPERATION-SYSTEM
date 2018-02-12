import os
import ipgetter

MY_IP = ipgetter.myip()
FOLDER_NAME = "system_folder"
MAIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
CHANGE_PASSWORD_FILE = MAIN_FOLDER + "/change_windows_password.py "
SYSTEM_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), FOLDER_NAME)
FILE_LIST_DIRECTORY = 1
BUFFER = 1024
FILE_ADDED_ACTION = "1"
FILE_DELETED_ACTION = "2"
FILE_MODIFIED_ACTION = "3"
READING = "rb"
WRITING = "wb"
FILE_BUFFER = 3000000
COUNTRY = "IL"
CITY = "Ramat Gan"

CLOUD_HOST = "0.0.0.0"
CLOUD_IP = "127.0.0.1"
CLOUD_PORT = 8820
NUMBER_OF_CLIENTS = 1
CLOUD = "cloud"
CLOUD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), CLOUD)

SEPARATOR = "#"

CLOCK_PORT = 8822
SYNC_PORT = 8824
NOTES_PORT = 8826

WEEK_DAYS_DICT = {6: "Sunday", 0: "Monday", 1: "Tuesday",
                  2: "Wednesday", 3: "Thursday",
                  4: "Friday", 5: "Saturday"}

WEATHER_DAY_STATUS = {"Clear": "pictures/sun_day.jpg", "Rain": "pictures/rain.jpg",
                      "Clouds": "pictures/cloud_day.jpg", "Default": "pictures/clouds.jpg"}

WEATHER_NIGHT_STATUS = {"Clear": "pictures/sun_night.jpg", "Rain": "pictures/rain.jpg",
                        "Clouds": "pictures/cloud_night.ico"}

DEFAULT = "Default"
SPACES = " "*21
SPACESS = " "*30
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

WINDOWS_JOIN = "\\"
SOFTWARES_FOLDER = "softwares/"
FILES_EXTENSIONS = [".txt", ".mp4", ".avi", ".mov", ".wav", ".jpg", ".png"]
MEDIA_EXTS = [".mp4", ".avi", ".mov", ".wav"]
PHOTO_EXTS = [".jpg", ".png"]
PYTHON = "python"
SUB_DIR = {"txt": "TextEditor"}
SUB_DIR.update(dict.fromkeys(["mp4", "avi", "mov", "wav"], "MediaPlayer"))
SUB_DIR.update(dict.fromkeys(["jpg", "png"], "PhotoViewer"))
SOFTWARE_DICT = {"txt": "TextEditor.py"}
SOFTWARE_DICT.update(dict.fromkeys(["mp4", "avi", "mov", "wav"], "MediaPlayer.py"))
SOFTWARE_DICT.update(dict.fromkeys(["jpg", "png"], "PhotoViewer.py"))
MEDIA_PLAYER_SOFTWARE = "MediaPlayer.py"
MEDIA_PLAYER_FOLDER = "softwares/MediaPlayer"
TXTEXT = ".txt"
REGULAR_WRITING = "w"
TXT_TITLE = "TEXT EDITOR -> "
TXT_SIZE = (1000, 800)
TXT_ICON = "txt.ico"
EDITOR_IMAGE = "txt.png"
FILE_NAME = "FILE NAME"
NULL = "null"

CLOSE_CLOCK_NOW = "CLOSE CLOCK NOW"
CLOSE_SYNC_NOW = "CLOSE SYNC NOW"
CLOSE_NOTES_NOW = "CLOSE NOTES NOW"

CLOSE_SOUND = "sounds/close_sound.wav"

SCREEN_PROGRAM = "CloudedOperationSystem.py"
CLOCK_PROGRAM = "clock.py"
NOTES_PROGRAM = "notes.py"
CALCULATOR_PROGRAM = "softwares/calculator/calculator.py"

VERIFICATION = "VERIFICATION"
NONE = "NONE"
EXISTS = "EXISTS"
NOT_EXISTS = "NOT EXISTS"
SEND = "SEND"
NOT_SEND = "NOT SEND"
DONE_VERIFICATION = "DONE VERIFICATION"

CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = 'https://www.googleapis.com/auth/calendar'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
TIME_ZONE = "Asia/Jerusalem"
YEAR = "Year"
MONTH = "Month"
DAYY = "Day"
HOURS = "Hours"
MINUTES = "Minutes"
SECONDS = "Seconds"
NONEE = "None"
METHOD = "Method"
BEFORE = "Before"
TIME_SEPARATOR = "T"
