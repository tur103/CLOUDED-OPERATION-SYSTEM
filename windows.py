from kivy.uix.screenmanager import Screen
from Tkinter import Tk
from tkFileDialog import askopenfilename
import sys, os, traceback, types, ctypes
import win32api, win32con, win32event, win32process
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon
import getpass
from win32com import adsi
from constants import *


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

    def get_user_name(self):
        self.username.text = getpass.getuser()

    def change_password(self):
        if self.password.text:
            if not self.isUserAdmin():
                self.runAsAdmin()
            else:
                username = self.get_username()
                password = self.password.text
                self.set_password(username, password)
            self.password.text = ""

    def remove_password(self):
        self.password.text = ""
        if not self.isUserAdmin():
            self.runAsAdmin()
        else:
            username = self.get_username()
            password = ""
            self.set_password(username, password)

    def get_username(self):
        return getpass.getuser()

    def set_password(self, username, password):
        ads_obj = adsi.ADsGetObject("WinNT://localhost/%s,user" % username)
        ads_obj.SetPassword(password)

    def isUserAdmin(self):
        return ctypes.windll.shell32.IsUserAnAdmin()

    def runAsAdmin(self, cmdLine=None, wait=True):
        python_exe = sys.executable
        cmdLine = [python_exe] + sys.argv
        cmd = '"%s"' % (cmdLine[0],)
        params = CHANGE_PASSWORD_FILE + self.password.text
        cmdDir = ''
        showCmd = win32con.SW_SHOWNORMAL
        lpVerb = 'runas'
        procInfo = ShellExecuteEx(nShow=showCmd,
                                  fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                  lpVerb=lpVerb,
                                  lpFile=cmd,
                                  lpParameters=params)
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
