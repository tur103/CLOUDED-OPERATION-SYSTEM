"""
Author          :   Or Israeli
FileName        :   SoftwareDetection.py
Date            :   1.12.17
Version         :   1.0
Description     :   Class that receives the chosen file and sends it
                    to the correct software by it's format.
"""
import subprocess
from constants import *
from threading import Thread


class SoftwareDetection(Thread):
    def __init__(self, file_name):
        Thread.__init__(self)
        self.file_name = file_name
        self.format = None
        self.start()

    def run(self):
        """

        The function detects the format of the file from it's name.

        """
        self.format = self.file_name.split("\\")[-1].split(".")[-1]
        self.execute_software()

    def execute_software(self):
        """

        The function decides which is the correct software to execute
        the file according to it's format and sends the command.

        """
        subprocess.call(" ".join([PYTHON, SOFTWARE_DICT[self.format], self.file_name]))
