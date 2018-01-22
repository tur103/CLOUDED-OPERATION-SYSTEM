from __future__ import division
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.config import Config
import kivy
import math


class CalculatorApp(App):
    def build(self):
        self.title = 'Calculator'
        self.icon = 'pictures/COS.png'


class CalculatorScreen(Screen):

    upper_string = ""
    lower_string = "0"
    arithmetic = False
    equal = False

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(CalculatorScreen, self).add_widget(*args)

    def digit_clicked(self, digit):
        if CalculatorScreen.arithmetic or CalculatorScreen.equal:
            CalculatorScreen.lower_string = "0"
        if CalculatorScreen.lower_string == "0" and digit != ".":
            CalculatorScreen.lower_string = digit
        else:
            CalculatorScreen.lower_string += digit
        CalculatorScreen.arithmetic = False
        CalculatorScreen.equal = False
        self.clicked()

    def arithmetic_clicked(self, arithmetic):
        if CalculatorScreen.arithmetic:
            if arithmetic != CalculatorScreen.upper_string[-2]:
                CalculatorScreen.upper_string = CalculatorScreen.upper_string[:-2]
                CalculatorScreen.upper_string += " " + arithmetic
        else:
            CalculatorScreen.upper_string += " " + CalculatorScreen.lower_string
            CalculatorScreen.lower_string = self.arithmetic_calculate()
            CalculatorScreen.upper_string += " " + arithmetic
            CalculatorScreen.arithmetic = True
            CalculatorScreen.equal = False
        self.clicked()

    def equal_clicked(self):
        CalculatorScreen.upper_string += " " + CalculatorScreen.lower_string
        CalculatorScreen.lower_string = self.arithmetic_calculate()
        CalculatorScreen.upper_string = ""
        CalculatorScreen.equal = True
        self.clicked()

    def back_clicked(self):
        if not CalculatorScreen.arithmetic and not CalculatorScreen.equal:
            if CalculatorScreen.lower_string != "0":
                if len(CalculatorScreen.lower_string):
                    CalculatorScreen.lower_string = CalculatorScreen.lower_string[:-1]
                    if not len(CalculatorScreen.lower_string):
                        CalculatorScreen.lower_string = "0"
        self.clicked()

    def clear_clicked(self):
        CalculatorScreen.lower_string = "0"
        self.clicked()

    def clear_all_clicked(self):
        CalculatorScreen.lower_string = "0"
        CalculatorScreen.upper_string = ""
        self.clicked()

    def negative_clicked(self):
        if CalculatorScreen.lower_string[0] == "-":
            CalculatorScreen.lower_string = CalculatorScreen.lower_string[1:]
        else:
            CalculatorScreen.lower_string = "-" + CalculatorScreen.lower_string
        CalculatorScreen.arithmetic = False
        self.clicked()

    def square_clicked(self):
        CalculatorScreen.lower_string = str(math.sqrt(float(CalculatorScreen.lower_string)))
        CalculatorScreen.arithmetic = False
        self.clicked()

    def one_divided_by_clicked(self):
        CalculatorScreen.lower_string = str(1 / float(CalculatorScreen.lower_string))
        CalculatorScreen.arithmetic = False
        self.clicked()

    def percent_clicked(self):
        if CalculatorScreen.upper_string:
            CalculatorScreen.lower_string = str(eval(CalculatorScreen.upper_string[:-2]) / 100 * float(CalculatorScreen.lower_string))
            CalculatorScreen.arithmetic = False
        self.clicked()

    @staticmethod
    def arithmetic_calculate():
        return str(eval(CalculatorScreen.upper_string))

    def clicked(self):
        self.upper_string.text = CalculatorScreen.upper_string
        self.lower_string.text = CalculatorScreen.lower_string


kivy.require('1.9.0')
Config.set('graphics', 'width', '280')
Config.set('graphics', 'height', '380')
Config.set('kivy', 'window_icon', 'pictures/COS.ico')
CalculatorApp().run()