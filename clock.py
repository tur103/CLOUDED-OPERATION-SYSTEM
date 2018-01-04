from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout
from math import cos, sin, pi
from kivy.clock import Clock
from kivy.lang import Builder
import thread
import datetime
import kivy
from kivy.config import Config
from constants import *
import socket


kv = '''
#:import math math

[ClockNumber@Label]:
    text: str(ctx.i)
    pos_hint: {"center_x": 0.5+0.42*math.sin(math.pi/6*(ctx.i-12)), "center_y": 0.5+0.42*math.cos(math.pi/6*(ctx.i-12))}
    font_size: self.height/16

<MyClockWidget>:
    face: face
    ticks: ticks
    FloatLayout:
        id: face
        size_hint: None, None
        pos_hint: {"center_x":0.5, "center_y":0.5}
        size: 0.9*min(root.size), 0.9*min(root.size)
        canvas.before:
            Color:
                rgb: .6, .6, .6
            Rectangle:
                size: root.size
                source: 'pictures/clock_background.jpg'
        canvas:
            Color:
                rgb: 0.1, 0.1, 0.1
            Ellipse:
                size: self.size     
                pos: self.pos
        ClockNumber:
            i: 1
        ClockNumber:
            i: 2
        ClockNumber:
            i: 3
        ClockNumber:
            i: 4
        ClockNumber:
            i: 5
        ClockNumber:
            i: 6
        ClockNumber:
            i: 7
        ClockNumber:
            i: 8
        ClockNumber:
            i: 9
        ClockNumber:
            i: 10
        ClockNumber:
            i: 11
        ClockNumber:
            i: 12
    Ticks:
        id: ticks
        r: min(root.size)*0.9/2
'''
Builder.load_string(kv)


class MyClockWidget(FloatLayout):
    pass


class Ticks(Widget):
    def __init__(self, **kwargs):
        super(Ticks, self).__init__(**kwargs)
        self.bind(pos=self.update_clock)
        self.bind(size=self.update_clock)

    def update_clock(self, *args):
        self.canvas.clear()
        with self.canvas:
            time = datetime.datetime.now()
            Color(0.2, 0.5, 0.2)
            Line(points=[self.center_x, self.center_y, self.center_x+0.8*self.r*sin(pi/30*time.second), self.center_y+0.8*self.r*cos(pi/30*time.second)], width=1, cap="round")
            Color(0.3, 0.6, 0.3)
            Line(points=[self.center_x, self.center_y, self.center_x+0.7*self.r*sin(pi/30*time.minute), self.center_y+0.7*self.r*cos(pi/30*time.minute)], width=2, cap="round")
            Color(0.4, 0.7, 0.4)
            th = time.hour*60 + time.minute
            Line(points=[self.center_x, self.center_y, self.center_x+0.5*self.r*sin(pi/360*th), self.center_y+0.5*self.r*cos(pi/360*th)], width=3, cap="round")


class MyClockApp(App):
    def build(self):
        clock = MyClockWidget()
        Clock.schedule_interval(clock.ticks.update_clock, 1)
        return clock


def stop_clock():
    server_socket = socket.socket()
    server_socket.bind((CLOUD_HOST, CLOCK_PORT))
    server_socket.listen(NUMBER_OF_CLIENTS)
    client_socket, addredd = server_socket.accept()
    if client_socket.recv(BUFFER) == CLOSE_CLOCK_NOW:
        client_socket.close()
        os._exit(0)


if __name__ == "__main__":
    kivy.require('1.9.0')
    Config.set('graphics', 'width', '300')
    Config.set('graphics', 'height', '300')
    Config.set('graphics', 'borderless', '1')
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'left', 900)
    Config.set('graphics', 'top', 135)
    Config.set('graphics', 'show_cursor', 0)
    Config.set('kivy', 'window_icon', 'pictures/clock.png')
    thread.start_new_thread(stop_clock, ())
    MyClockApp().run()
