"""
Author          :   Or Israeli
FileName        :   automatically_cloud_synchronization.py
Date            :   3.11.17
Version         :   1.0
Description     :   A program that synchronizes the files from
                    the system's folder automatically with the cloud.
"""
from constants import *
import win32file
from win32con import *
import socket
import time


def automatically_cloud_synchronization():
    system_folder_creation = win32file.CreateFile(SYSTEM_FOLDER, FILE_LIST_DIRECTORY, FILE_SHARE_READ,
                                                  None, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, None)
    waiting_for_change(system_folder_creation)


def waiting_for_change(system_folder_creation):
    """

    The function waits till a change appeared in the system's folder.
    A new file was added, a file was deleted or a file was modified
    by the user. The function catches all the cases.

    Args:
        system_folder_creation (CreateFile object): The system folder for detecting changes on.

    """
    while True:
        action, file_name = win32file.ReadDirectoryChangesW(system_folder_creation, BUFFER, True,
                                                            FILE_NOTIFY_CHANGE_FILE_NAME |
                                                            FILE_NOTIFY_CHANGE_LAST_WRITE)[0]
        synchronize_the_changes(action, file_name)


def synchronize_the_changes(action, file_name):
    """

    The function receives the change that occurred
    and synchronize it with the cloud.

    Args:
        action (int): The action number of the change. file was added,
                      file was deleted or file was modified.
        file_name (string): The name of the file that was changed.

    """
    socket = open_connection_with_the_cloud()
    socket.send(SEPARATOR.join([MY_IP, str(action), file_name]))
    if str(action) == FILE_MODIFIED_ACTION:
        with open(os.path.join(SYSTEM_FOLDER, file_name), READING) as modified_file:
            time.sleep(0.3)
            socket.send(modified_file.read())
    socket.close()


def create_system_folder():
    """

    The function checks if the system folder is exists in the user's
    computer. If not it creates a new one.

    """
    if not os.path.exists(SYSTEM_FOLDER):
        os.mkdir(SYSTEM_FOLDER)


def open_connection_with_the_cloud():
    """

    The function opens a socket connection with the server
    cloud for synchronization.

    Returns:
        (socket): the socket connection with the cloud.

    """
    client_socket = socket.socket()
    client_socket.connect((CLOUD_IP, CLOUD_PORT))
    return client_socket


if __name__ == '__main__':
    create_system_folder()
    automatically_cloud_synchronization()
