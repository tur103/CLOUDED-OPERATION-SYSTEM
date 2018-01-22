from date_and_time import *
from SoftwareDetection import *
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from system_user_calculator import *


class HomeScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(HomeScreen, self).add_widget(*args)

    def selection_updated(self, selection):
        if selection:
            file_name = selection[0]
            if file_name.endswith(tuple(FILES_EXTENSIONS)):
                software = SoftwareDetection(file_name)

    def get_picture(self):
        status, part_of_day = DateAndTime.get_weather_status()
        try:
            if part_of_day == DAY:
                return WEATHER_DAY_STATUS[status]
            else:
                return WEATHER_NIGHT_STATUS[status]
        except KeyError:
            return WEATHER_DAY_STATUS[DEFAULT]

    def get_date(self):
        date = DateAndTime.get_date()
        day = DateAndTime.get_day()
        temperatures = DateAndTime.get_temperature()
        return date + SPACES + day + DOWNLINES + SPACESS + temperatures + CELSIUS_SIGN

    def get_folder(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), FOLDER_NAME).lower()

    def open_calculator(self):
        SystemUserCalculator()
