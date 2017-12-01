"""
Author          :   Or Israeli
FileName        :   TextEditor.py
Date            :   1.12.17
Version         :   1.0
Description     :   Text Editor software for editing txt format file.
"""
from kivy.app import App
import sys
from kivy.uix.screenmanager import Screen
from constants import *
import os


class TxtFile(Screen):
    def __init__(self):
        super(TxtFile, self).__init__()
        self.file_name = sys.argv[1]
        self.data = None

    def get_file_name(self):
        """

        The function adds the name of the text file to the editor.

         Returns:
            string: The name of the text file.

        """
        return self.file_name.split(WINDOWS_JOIN)[-1].split(FILES_EXTENSIONS[0])[0]

    def get_text(self):
        """

        The function adds the current data of the text file to the editor.

        Returns:
            string: The current data of the text file.

        """
        with open(self.file_name, READING) as file_handle:
            self.data = file_handle.read()
            return self.data

    def change_file_name(self, file_name):
        new_file_name = "\\".join(self.file_name.split("\\")[:-1] + [file_name + TXTEXT])
        os.rename(self.file_name, new_file_name)
        self.file_name = new_file_name

    def change_file_data(self, file_data):
        print file_data
        with open(self.file_name, REGULAR_WRITING) as file_handle:
            self.data = file_data
            file_handle.write(self.data)


class TextEditorApp(App):
    pass

TextEditorApp().run()
