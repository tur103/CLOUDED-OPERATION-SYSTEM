from kivy.uix.screenmanager import Screen
from Tkinter import Tk
from tkFileDialog import askopenfilename
import ctypes


class WindowsScreen(Screen):

    chosen_background_image = ""

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(WindowsScreen, self).add_widget(*args)

    def open_explorer(self):
        Tk().withdraw()
        WindowsScreen.chosen_background_image = askopenfilename(filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        if WindowsScreen.chosen_background_image:
            self.background.text = WindowsScreen.chosen_background_image.split("/")[-1]

    def change_background_image(self):
        if WindowsScreen.chosen_background_image:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, WindowsScreen.chosen_background_image, 0)
