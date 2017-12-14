"""
Author          :   Or Israeli
FileName        :   cloud.py
Date            :   3.11.17
Version         :   1.0
Description     :   The cloud of the operation system. The cloud save al the
                    user's files and synchronize with the changes automatically.
"""
import socket
from constants import *


class Cloud(object):
    def __init__(self):
        object.__init__(self)
        self.create_cloud_folder()
        self.cloud()

    def cloud(self):
        """

        The cloud waits until a change request received.
        according to the change the cloud updates the user's
        folder and saves the changes that the user did.

        """
        cloud_socket = socket.socket()
        cloud_socket.bind((CLOUD_HOST, CLOUD_PORT))
        cloud_socket.listen(NUMBER_OF_CLIENTS)
        while True:
            client_socket, address = cloud_socket.accept()
            change_details = client_socket.recv(BUFFER)
            client_ip, action, file_name = change_details.split(SEPARATOR)
            self.create_client_folder(client_ip)
            client_folder = os.path.join(CLOUD_FOLDER, client_ip)
            if action == FILE_ADDED_ACTION:
                with open(os.path.join(client_folder, file_name), WRITING):
                    pass
            elif action == FILE_DELETED_ACTION:
                os.remove(os.path.join(client_folder, file_name))
            elif action == FILE_MODIFIED_ACTION:
                file_data = client_socket.recv(FILE_BUFFER)
                with open(os.path.join(client_folder, file_name), WRITING) as modified_file:
                    modified_file.write(file_data)
            elif action == VERIFICATION:
                self.execute_verification(client_socket, client_folder)
            client_socket.close()

    def execute_verification(self, client_socket, client_folder):
        files_list = os.listdir(client_folder)
        done = True
        while done:
            file_name = client_socket.recv(BUFFER)
            if file_name == DONE_VERIFICATION:
                done = False
            elif file_name in files_list:
                files_list.remove(file_name)
                client_socket.send(EXISTS)
                received = client_socket.recv(FILE_BUFFER)
                with open(os.path.join(client_folder, file_name), READING) as file_handler:
                    data = file_handler.read()
                if file_name.endswith(tuple(MEDIA_EXTS)) or file_name.endswith(tuple(PHOTO_EXTS)):
                    if received == str(len(data)):
                        client_socket.send(EXISTS)
                    else:
                        client_socket.send(NOT_EXISTS)
                        received = client_socket.recv(FILE_BUFFER)
                        self.create_new_file(os.path.join(client_folder, file_name), received)
                else:
                    if received == data:
                        client_socket.send(EXISTS)
                    else:
                        client_socket.send(NOT_EXISTS)
                        self.create_new_file(os.path.join(client_folder, file_name), received)
            else:
                client_socket.send(NOT_EXISTS)
                received = client_socket.recv(FILE_BUFFER)
                self.create_new_file(os.path.join(client_folder, file_name), received)

        for removed_file in files_list:
            os.remove(os.path.join(client_folder, removed_file))

    @staticmethod
    def create_new_file(path, data):
        file_handler = open(path, WRITING)
        file_handler.write(data)
        file_handler.close()

    @staticmethod
    def create_cloud_folder():
        """

        The function checks if the cloud folder is exists.
        If not it creates a new one.

        """
        if not os.path.exists(CLOUD_FOLDER):
            os.mkdir(CLOUD_FOLDER)

    @staticmethod
    def create_client_folder(client_ip):
        """

        The function checks if the client has a folder on the cloud.
        If not it creates a new one.

        Args:
            client_ip (string): The ip of the client.

        """
        if not os.path.exists(os.path.join(CLOUD_FOLDER, client_ip)):
            os.mkdir(os.path.join(CLOUD_FOLDER, client_ip))


Cloud()
