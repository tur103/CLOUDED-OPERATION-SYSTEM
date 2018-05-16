from kivy.uix.screenmanager import Screen
from Tkinter import Tk
from tkFileDialog import askopenfilename, askdirectory
import sys, os, traceback, types, ctypes
import win32api, win32con, win32event, win32process
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon
import getpass
from win32com import adsi
from constants import *
import win32clipboard
import win32com.client


class WindowsScreen(Screen):

    chosen_background_image = ""
    chosen_hidden_file = ""
    chosen_hidden_folder = ""
    chosen_original_file = ""
    chosen_destination_folder = ""

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(WindowsScreen, self).add_widget(*args)

    def open_explorer(self):
        """

        Opens the windows explorer so the user will choose a file from the disk.

        """
        Tk().withdraw()
        WindowsScreen.chosen_background_image = askopenfilename(title="Pick an Image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        if WindowsScreen.chosen_background_image:
            self.background.text = WindowsScreen.chosen_background_image.split("/")[-1]

    def change_background_image(self):
        """

        Changes the windows background image for the photo that the user chose.

        """
        if WindowsScreen.chosen_background_image:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, WindowsScreen.chosen_background_image, 0)
            WindowsScreen.chosen_background_image = ""
            self.background.text = ""

    def get_user_name(self):
        """

        Gets the windows user name of the user.

        """
        self.username.text = getpass.getuser()

    def change_password(self):
        """

        Changes the windows password of the user for the given text.

        """
        if self.password.text:
            if not self.isUserAdmin():
                self.runAsAdmin()
            else:
                username = self.get_username()
                password = self.password.text
                self.set_password(username, password)
            self.password.text = ""

    def remove_password(self):
        """

        Removes the windows password from the user's computer.

        """
        self.password.text = ""
        if not self.isUserAdmin():
            self.runAsAdmin()
        else:
            username = self.get_username()
            password = ""
            self.set_password(username, password)

    def get_username(self):
        """

        Gets the windows user name of the user.

        returns:
            string: The windows user name.

        """
        return getpass.getuser()

    def set_password(self, username, password):
        """

        Changes the windows password of the user for the given text.

        args:
            username (string): The user name of the user.
            password (string): The new password of the user.

        """
        ads_obj = adsi.ADsGetObject("WinNT://localhost/%s,user" % username)
        ads_obj.SetPassword(password)

    def isUserAdmin(self):
        """

        Checks if the file executed as admin.

        returns:
            bool: true or false.

        """
        return ctypes.windll.shell32.IsUserAnAdmin()

    def runAsAdmin(self, cmdLine=None, wait=True):
        """

        Executes the file again as admin.

        """
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

    def copy_to_clipboard(self):
        """

        Copying the given text from the user to the
        clipboard.

        """
        if self.copy.text:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(self.copy.text)
            win32clipboard.CloseClipboard()
            self.copy.text = ""

    def paste_from_clipboard(self):
        """

        pasting the text from the clipboard to the
        screen.

        """
        win32clipboard.OpenClipboard()
        self.paste.text = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

    def pick_file(self):
        """

        Opens the windows explorer so the user will choose a file from the disk.

        """
        Tk().withdraw()
        WindowsScreen.chosen_hidden_file = askopenfilename(title="Pick a File")
        if WindowsScreen.chosen_hidden_file:
            self.file.text = WindowsScreen.chosen_hidden_file.split("/")[-1]
            self.folder.text = "Pick a Folder"
            WindowsScreen.chosen_hidden_folder = ""

    def pick_folder(self):
        """

        Opens the windows explorer so the user will choose a folder from the disk.

        """
        Tk().withdraw()
        WindowsScreen.chosen_hidden_folder = askdirectory(title="Pick a Folder")
        if WindowsScreen.chosen_hidden_folder:
            self.folder.text = WindowsScreen.chosen_hidden_folder.split("/")[-1]
            self.file.text = "Pick a File"
            WindowsScreen.chosen_hidden_file = ""

    def make_file_hidden(self):
        """

        Gets a file or a folder from the user and makes
        them as hidden.

        """
        if WindowsScreen.chosen_hidden_file:
            ctypes.windll.kernel32.SetFileAttributesW(WindowsScreen.chosen_hidden_file, 0x02)
            WindowsScreen.chosen_hidden_file = ""
            self.file.text = "Pick a File"
        elif WindowsScreen.chosen_hidden_folder:
            ctypes.windll.kernel32.SetFileAttributesW(WindowsScreen.chosen_hidden_folder, 0x02)
            WindowsScreen.chosen_hidden_folder = ""
            self.folder.text = "Pick a Folder"

    def original_file(self):
        """

        Opens the windows explorer so the user will choose a file from the disk.

        """
        Tk().withdraw()
        WindowsScreen.chosen_original_file = askopenfilename(title="Pick Original File")
        if WindowsScreen.chosen_original_file:
            self.original.text = WindowsScreen.chosen_original_file.split("/")[-1]

    def destination_folder(self):
        """

        Opens the windows explorer so the user will choose a folder from the disk.

        """
        Tk().withdraw()
        WindowsScreen.chosen_destination_folder = askdirectory(title="Pick Destination Folder")
        if WindowsScreen.chosen_destination_folder:
            self.destination.text = WindowsScreen.chosen_destination_folder.split("/")[-1]

    def create_shortcut(self):
        """

        Creating a shortcut file of a given file from the
        user into a given folder.

        """
        if WindowsScreen.chosen_original_file and WindowsScreen.chosen_destination_folder:
            shell = win32com.client.Dispatch("Wscript.shell")
            shortcut_file = os.path.join(WindowsScreen.chosen_destination_folder,
                                         WindowsScreen.chosen_original_file.split("/")[-1] + ".lnk")
            shortcut = shell.CreateShortCut(shortcut_file)
            shortcut.targetpath = WindowsScreen.chosen_original_file
            shortcut.save()
            WindowsScreen.chosen_original_file = ""
            WindowsScreen.chosen_destination_folder = ""
            self.original.text = "Original File"
            self.destination.text = "Destination Folder"
