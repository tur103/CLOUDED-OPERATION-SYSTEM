from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from date_and_time import *
from SoftwareDetection import *
import kivy
from kivy.config import Config
from playsound import playsound
import socket


from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import urllib2
import json
import ctypes
import httplib2

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)

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


class CalendarScreen(Screen):
    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(CalendarScreen, self).add_widget(*args)

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print 'Storing credentials to ' + credential_path
        return credentials

    def get_time_zone(self):
        f = urllib2.urlopen('http://freegeoip.net/json/')
        json_string = f.read()
        f.close()
        location = json.loads(json_string)
        time_zone = location["time_zone"]
        if not time_zone:
            time_zone = TIME_ZONE
        return time_zone

    def new_event(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        title, location, description, time_zone, start_date_time, end_date_time,\
        recurrence, reminder_method, reminder_time = self.get_event_details()
        event = {
          'summary': title,
          'location': location,
          'description': description,
          'start': {
            'dateTime': start_date_time,
            'timeZone': time_zone,
          },
          'end': {
            'dateTime': end_date_time,
            'timeZone': time_zone,
          },
          'recurrence': [
              recurrence
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': reminder_method, 'minutes': reminder_time},
            ],
          },
        }

        service.events().insert(calendarId='primary', body=event).execute()
        self.clear_interface()

    def get_event_details(self):
        title = self.title.text
        location = self.location.text
        description = self.description.text
        time_zone = self.time_zone.text
        start_year = self.start_year.text if self.start_year.text != YEAR else "2018"
        start_month = self.start_month.text if self.start_month.text != MONTH else "01"
        start_day = self.start_day.text if self.start_day.text != DAYY else "01"
        start_hour = self.start_hour.text if self.start_hour.text != HOURS else "00"
        start_minute = self.start_minute.text if self.start_minute.text != MINUTES else "00"
        start_second = self.start_second.text if self.start_second.text != SECONDS else "00"
        start_date_time = "-".join([start_year, start_month, start_day]) + TIME_SEPARATOR + \
                          ":".join([start_hour, start_minute, start_second])
        end_year = self.end_year.text if self.end_year.text != YEAR else "2018"
        end_month = self.end_month.text if self.end_month.text != MONTH else "01"
        end_day = self.end_day.text if self.end_day.text != DAYY else "01"
        end_hour = self.end_hour.text if self.end_hour.text != HOURS else "00"
        end_minute = self.end_minute.text if self.end_minute.text != MINUTES else "00"
        end_second = self.end_second.text if self.end_second.text != SECONDS else "00"
        end_date_time = "-".join([end_year, end_month, end_day]) + TIME_SEPARATOR + \
                        ":".join([end_hour, end_minute, end_second])
        recurrence = 'RRULE:FREQ=' + self.recurrence.text if self.recurrence.text != NONEE else None
        reminder_method = self.reminder_method.text if self.reminder_method.text != METHOD \
            and self.reminder_method.text != NONEE else None
        reminder_time = self.reminder_time.text if self.reminder_time.text != BEFORE \
            and self.reminder_time.text != NONEE else None
        if not reminder_method or not reminder_time:
            reminder_method, reminder_time = "popup", 0
        else:
            if "minutes" in reminder_time:
                reminder_time = reminder_time.replace(" minutes", "")
                reminder_time = int(reminder_time)
            elif "hours" in reminder_time:
                reminder_time = reminder_time.replace(" hours", "")
                reminder_time = int(reminder_time) * 60
            elif "days" in reminder_time:
                reminder_time = reminder_time.replace(" days", "")
                reminder_time = int(reminder_time) * 1440
            elif "weeks" in reminder_time:
                reminder_time = reminder_time.replace(" weeks", "")
                reminder_time = int(reminder_time) * 10080
        return title, location, description, time_zone, start_date_time, end_date_time,\
               recurrence, reminder_method, reminder_time

    def clear_interface(self):
        self.title.text = ""
        self.location.text = ""
        self.description.text = ""
        self.start_year.text = "Year"
        self.start_month.text = "Month"
        self.start_day.text = "Day"
        self.start_hour.text = "Hours"
        self.start_minute.text = "Minutes"
        self.start_second.text = "Seconds"
        self.end_year.text = "Year"
        self.end_month.text = "Month"
        self.end_day.text = "Day"
        self.end_hour.text = "Hours"
        self.end_minute.text = "Minutes"
        self.end_second.text = "Seconds"
        self.recurrence.text = "None"
        self.reminder_method.text = "Method"
        self.reminder_time.text = "Before"

    def show_upcoming_events(self):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        list_of_events = []
        for event in events:
            list_of_events.append(event['summary'] + "  " + event['start'].get('dateTime', event['start'].get('date')))
        return list_of_events


class ShowcaseApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def build(self):
        self.title = 'CLOUDED OPERATION SYSTEM'
        self.icon = 'pictures/COS.png'
        self.screens = {}
        self.available_screens = ['CLOUDED OPERATION SYSTEM', 'CALENDAR']
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.go_next_screen()

    def on_stop(self):
        self.close_clock()
        self.close_sync()
        self.close_notes()
        self.close_sound()

    @staticmethod
    def close_clock():
        client_socket = socket.socket()
        client_socket.connect((CLOUD_IP, CLOCK_PORT))
        client_socket.send(CLOSE_CLOCK_NOW)
        client_socket.close()

    @staticmethod
    def close_sync():
        client_socket = socket.socket()
        client_socket.connect((CLOUD_IP, SYNC_PORT))
        client_socket.send(CLOSE_SYNC_NOW)
        client_socket.close()

    @staticmethod
    def close_notes():
        client_socket = socket.socket()
        client_socket.connect((CLOUD_IP, NOTES_PORT))
        client_socket.send(CLOSE_NOTES_NOW)
        client_socket.close()

    @staticmethod
    def close_sound():
        playsound(CLOSE_SOUND)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        self.update_sourcecode()

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

    def read_sourcecode(self):
        fn = self.available_screens[self.index]
        with open(fn) as fd:
            return fd.read()

    def toggle_source_code(self):
        self.show_sourcecode = not self.show_sourcecode
        if self.show_sourcecode:
            height = self.root.height * .3
        else:
            height = 0

        Animation(height=height, d=.3, t='out_quart').start(
                self.root.ids.sv)

        self.update_sourcecode()

    def update_sourcecode(self):
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1

    def showcase_floatlayout(self, layout):
        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 5:
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
#:import random random.random
Button:
    size_hint: random(), random()
    pos_hint: {'x': random(), 'y': random()}
    text:
        'size_hint x: {} y: {}\\n pos_hint x: {} y: {}'.format(\
            self.size_hint_x, self.size_hint_y, self.pos_hint['x'],\
            self.pos_hint['y'])
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_boxlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 5:
                layout.orientation = 'vertical'\
                    if layout.orientation == 'horizontal' else 'horizontal'
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_gridlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 15:
                layout.rows = 3 if layout.rows is None else None
                layout.cols = None if layout.rows == 3 else 3
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text:
        'rows: {}\\ncols: {}'.format(self.parent.rows, self.parent.cols)\
        if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_stacklayout(self, layout):
        orientations = ('lr-tb', 'tb-lr',
                        'rl-tb', 'tb-rl',
                        'lr-bt', 'bt-lr',
                        'rl-bt', 'bt-rl')

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 11:
                layout.clear_widgets()
                cur_orientation = orientations.index(layout.orientation)
                layout.orientation = orientations[cur_orientation - 1]
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
    size_hint: .2, .2
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_anchorlayout(self, layout):

        def change_anchor(self, *l):
            if not layout.get_parent_window():
                return
            anchor_x = ('left', 'center', 'right')
            anchor_y = ('top', 'center', 'bottom')
            if layout.anchor_x == 'left':
                layout.anchor_y = anchor_y[anchor_y.index(layout.anchor_y) - 1]
            layout.anchor_x = anchor_x[anchor_x.index(layout.anchor_x) - 1]

            Clock.schedule_once(change_anchor, 1)
        Clock.schedule_once(change_anchor, 1)


kivy.require('1.9.0')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 85)
Config.set('graphics', 'top', 150)
Config.set('kivy', 'window_icon', 'pictures/COS.ico')
ShowcaseApp().run()
