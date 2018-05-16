import sys, os, traceback, types, ctypes
import win32api, win32con, win32event, win32process
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon
import getpass
from win32com import adsi
import sys


def main():
    if not isUserAdmin():
        runAsAdmin()
    if isUserAdmin():
        username = get_username()
        try:
            password = sys.argv[1]
        except:
            password = ""
        set_password(username, password)


def get_username():
    """

    Getting the windows user name of the user.

    returns:
        string: the windows user name of the user.

    """
    return getpass.getuser()


def set_password(username, password):
    """

    Sets a new windows password of the user.

    args:
        username (string): the windows user name.
        password (string): the new password for  windows.

    """
    ads_obj = adsi.ADsGetObject("WinNT://localhost/%s,user" % username)
    ads_obj.SetPassword(password)


def isUserAdmin():
    """

    Checks if the file executed as admin.

    returns:
        bool: true or false.

    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def runAsAdmin(cmdLine=None, wait=True):
    """

    Executes the file again as admin.

    """
    python_exe = sys.executable
    cmdLine = [python_exe] + sys.argv
    cmd = '"%s"' % (cmdLine[0],)
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
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


if __name__ == "__main__":
    main()
