from date_and_time import *
from SoftwareDetection import *
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from system_user_calculator import *
from database import *
import time


class HomeScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(HomeScreen, self).add_widget(*args)

    def selection_updated(self, selection):
        if selection:
            if selection == NULL:
                SoftwareDetection(selection)
            else:
                file_name = selection[0]
                if file_name.endswith(tuple(FILES_EXTENSIONS)):
                    SoftwareDetection(file_name)
                    if file_name.endswith(TXTEXT):
                        time.sleep(0.3)
                        self.refresh_last_edited()

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

    def get_last_edited(self, place):
        database = Database()
        return database.get_last_edited_table(True)[place - 1]

    def refresh_last_edited(self):
        self.first.text = self.get_last_edited(1)
        self.second.text = self.get_last_edited(2)
        self.third.text = self.get_last_edited(3)
        self.fourth.text = self.get_last_edited(4)
        self.fifth.text = self.get_last_edited(5)

    def execute_file(self, place):
        database = Database()
        self.selection_updated([database.get_last_edited_table()[place - 1]])
