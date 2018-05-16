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
import threading
import thread


class AutomaticallyCloudSynchronization(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.create_system_folder()
        self.system_folder_creation = win32file.CreateFile(SYSTEM_FOLDER, FILE_LIST_DIRECTORY, FILE_SHARE_READ,
                                                           None, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, None)
        self.start()

    def run(self):
        """

        Function that executing the sync steps.

        """
        thread.start_new_thread(self.stop_synchronization, ())
        self.execute_verification()
        self.waiting_for_change()

    def execute_verification(self):
        """

        Function that executing the verification and checks if
        the cloud is updated with all the files from the client folder.
        If not the cloud recieves the missing files.

        """
        client_socket = self.open_connection_with_the_cloud()
        client_socket.send(SEPARATOR.join([MY_IP, VERIFICATION, NONE]))
        directory_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), FOLDER_NAME)
        for exists_file in os.listdir(directory_name):
            client_socket.send(exists_file)
            with open(os.path.join(directory_name, exists_file), READING) as file_handler:
                    data = file_handler.read()
            if client_socket.recv(BUFFER) == EXISTS:
                if exists_file.endswith(tuple(MEDIA_EXTS)) or exists_file.endswith(tuple(PHOTO_EXTS)):
                    client_socket.send(str(len(data)))
                    to_send = SEND
                else:
                    client_socket.send(str(data))
                    time.sleep(0.3)
                    to_send = NOT_SEND
                if client_socket.recv(BUFFER) != EXISTS and to_send == SEND:
                    client_socket.send(data)
                    time.sleep(0.3)
            else:
                client_socket.send(data)
                time.sleep(0.3)

        client_socket.send(DONE_VERIFICATION)

    def stop_synchronization(self):
        """

        When the main screen shuts down the sync stops

        """
        server_socket = socket.socket()
        server_socket.bind((CLOUD_HOST, SYNC_PORT))
        server_socket.listen(NUMBER_OF_CLIENTS)
        client_socket, addredd = server_socket.accept()
        if client_socket.recv(BUFFER) == CLOSE_SYNC_NOW:
            client_socket.close()
            os._exit(0)

    def waiting_for_change(self):
        """

        The function waits till a change appeared in the system's folder.
        A new file was added, a file was deleted or a file was modified
        by the user. The function catches all the cases.

        """
        while True:
            action, file_name = win32file.ReadDirectoryChangesW(self.system_folder_creation, BUFFER, True,
                                                                FILE_NOTIFY_CHANGE_FILE_NAME |
                                                                FILE_NOTIFY_CHANGE_LAST_WRITE)[0]
            self.synchronize_the_changes(action, file_name)

    def synchronize_the_changes(self, action, file_name):
        """

        The function receives the change that occurred
        and synchronize it with the cloud.

        Args:
            action (int): The action number of the change. file was added,
                          file was deleted or file was modified.
            file_name (string): The name of the file that was changed.

        """
        socket = self.open_connection_with_the_cloud()
        socket.send(SEPARATOR.join([MY_IP, str(action), file_name]))
        if str(action) == FILE_MODIFIED_ACTION:
            with open(os.path.join(SYSTEM_FOLDER, file_name), READING) as modified_file:
                time.sleep(0.3)
                socket.send(modified_file.read())
        socket.close()

    @staticmethod
    def create_system_folder():
        """

        The function checks if the system folder is exists in the user's
        computer. If not it creates a new one.

        """
        if not os.path.exists(SYSTEM_FOLDER):
            os.mkdir(SYSTEM_FOLDER)

    @staticmethod
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
