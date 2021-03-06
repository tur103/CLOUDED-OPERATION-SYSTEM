from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
import kivy
from kivy.config import Config
from playsound import playsound
import socket
from home import *
from calendarr import *
from windows import *


class CloudedOperationSystemApp(App):

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
        self.available_screens = ['HOME', 'CALENDAR', 'WINDOWS']
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.go_next_screen()

    def on_stop(self):
        """

        Executes when the window is closed to close
        all the other functions of the program.

        """
        self.close_clock()
        self.close_sync()
        self.close_notes()
        self.close_sound()

    @staticmethod
    def close_clock():
        """

        Closing the clock screen.

        """
        client_socket = socket.socket()
        client_socket.connect((CLOUD_IP, CLOCK_PORT))
        client_socket.send(CLOSE_CLOCK_NOW)
        client_socket.close()

    @staticmethod
    def close_sync():
        """

        Closing the sync process.

        """
        client_socket = socket.socket()
        client_socket.connect((CLOUD_IP, SYNC_PORT))
        client_socket.send(CLOSE_SYNC_NOW)
        client_socket.close()

    @staticmethod
    def close_notes():
        """

        Closing the notes screen.

        """
        client_socket = socket.socket()
        client_socket.connect((CLOUD_IP, NOTES_PORT))
        client_socket.send(CLOSE_NOTES_NOW)
        client_socket.close()

    @staticmethod
    def close_sound():
        """

        Displaying the closing sound when the window is closed.

        """
        playsound(CLOSE_SOUND)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_current_title(self, instance, value):
        """

        Displaying the title of the window as the name of the screen.

        args:
            value (string): The name of the window.

        """
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        """

        Moving to the previous screen.

        """
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_next_screen(self):
        """

        Moving to the next screen.

        """
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_screen(self, idx):
        """

        Displaying the current screen on the window.

        args:
            idx (int): The index number of the current screen.

        """
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        self.update_sourcecode()

    def go_hierarchy_previous(self):
        """

        Moving to the previous selected screen.

        """
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        """

        Loading the graphic screen to the window
        from the kivi file.

        args:
            index: The index number of the current screen.

        """
        os.chdir(MAIN_FOLDER)
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
Config.set('graphics', 'top', 100)
Config.set('kivy', 'window_icon', 'pictures/COS.ico')
CloudedOperationSystemApp().run()
