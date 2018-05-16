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
        """

        Executes when the user selects a file
        and execute the selected file with the matching software.

        args:
            selection (string): The path to the selected file.

        """
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
                    elif file_name.endswith(tuple(MEDIA_EXTS)):
                        time.sleep(0.3)
                        self.refresh_fav_videos()

    def get_picture(self):
        """

        Getting the weather icon that matches to the current
        outside weather status and display it on the screen.

        returns:
            string: the path to the icon.

        """
        status, part_of_day = DateAndTime.get_weather_status()
        try:
            if part_of_day == DAY:
                return WEATHER_DAY_STATUS[status]
            else:
                return WEATHER_NIGHT_STATUS[status]
        except KeyError:
            return WEATHER_DAY_STATUS[DEFAULT]

    def get_date(self):
        """

        Gets the date and temperature of the current
        location and time and display it on the screen.

        return:
            string: The current date and weather.

        """
        date = DateAndTime.get_date()
        day = DateAndTime.get_day()
        temperatures = DateAndTime.get_temperature()
        return date + SPACES + day + DOWNLINES + SPACESS + temperatures + CELSIUS_SIGN

    def get_folder(self):
        """

        Generates the path for the system folder of the client.

        returns:
            string: The path for the system client folder.

        """
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), FOLDER_NAME).lower()

    def open_calculator(self):
        """

        Executes the calculator software.

        """
        SystemUserCalculator()

    def get_last_edited(self, place):
        """

        Gets and displays the last edited text files on the screen.

        args:
            place (int): The place of the file in the list.

        returns:
            string: The name of the text file.

        """
        database = Database()
        return database.get_last_edited_table(True)[place - 1]

    def refresh_last_edited(self):
        """

        Refreshing the last edited text files list after a new file opened.

        """
        self.first.text = self.get_last_edited(1)
        self.second.text = self.get_last_edited(2)
        self.third.text = self.get_last_edited(3)
        self.fourth.text = self.get_last_edited(4)
        self.fifth.text = self.get_last_edited(5)

    def execute_txt_file(self, place):
        """

        Executes the text editor software with a text file
        that was selected from the last edited text files list.

        args:
            place (int): The location of the file in the list.

        """
        database = Database()
        self.selection_updated([database.get_last_edited_table()[place - 1]])
        database.close_database()

    def get_fav_videos(self, place):
        """

        Gets and displays the favorite video files on the screen.

        args:
            place (int): The place of the file in the list.

        returns:
            string: The name of the video file.

        """
        database = Database()
        videos_list = database.get_fav_videos_list()
        if len(videos_list) >= place:
            return (videos_list[place - 1][0]).split("\\")[-1]
        else:
            return ""

    def refresh_fav_videos(self):
        """

        Refreshing the favorite video files list after a new file opened.

        """
        self.firstv.text = self.get_fav_videos(1)
        self.secondv.text = self.get_fav_videos(2)
        self.thirdv.text = self.get_fav_videos(3)
        self.fourthv.text = self.get_fav_videos(4)
        self.fifthv.text = self.get_fav_videos(5)

    def execute_video_file(self, place):
        """

        Executes the media player software with a video file
        that was selected from the favorite video files list.

        args:
            place (int): The location of the file in the list.

        """
        database = Database()
        self.selection_updated([database.get_fav_videos_list()[place - 1][0]])
        database.close_database()
