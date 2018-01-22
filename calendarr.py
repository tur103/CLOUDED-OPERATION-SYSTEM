from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import urllib2
import json
import ctypes
import httplib2
from kivy.uix.screenmanager import Screen
from constants import *


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


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
