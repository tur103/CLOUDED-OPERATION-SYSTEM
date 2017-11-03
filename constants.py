import os
import ipgetter

MY_IP = ipgetter.myip()
FOLDER_NAME = "c-o-s folder"
SYSTEM_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), FOLDER_NAME)
FILE_LIST_DIRECTORY = 1
BUFFER = 1024
FILE_ADDED_ACTION = 1
FILE_DELETED_ACTION = 2
FILE_MODIFIED_ACTION = 3
READING = "rb"
WRITING = "wb"
FILE_BUFFER = 300000

CLOUD_HOST = "0.0.0.0"
CLOUD_IP = "127.0.0.1"
CLOUD_PORT = 8820
NUMBER_OF_CLIENTS = 1
CLOUD = "cloud"
CLOUD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), CLOUD)

SEPARATOR = "#"