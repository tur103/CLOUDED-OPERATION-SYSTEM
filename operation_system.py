"""
Author          :   Or Israeli
FileName        :   operation_system.py
Date            :   3.11.17
Version         :   1.0
Description     :   The Clouded Operation System (COS).
                    Accessible and comfortable experience in file management
                    including automatically synchronization with an external cloud.
                    Every new file added, deleted or modified by the user will
                    be synchronized with the cloud and the changes will be automatically
                    saved. The system includes operation software for easy and quality file
                    operation with available but powerful interfaces.
"""
from automatically_cloud_synchronization import *
from system_user_screen import *
from system_user_clock import *


class OperationSystem(object):
    def __init__(self):
        object.__init__(self)
        self.operation_system()

    def operation_system(self):
        """

        The function runs the operation system.
        Displays the Graphic User Interface and process the automatically
        synchronization wint the cloud.

        """
        self.start_automatically_cloud_synchronization()
        self.start_system_user_screen()
        self.start_system_user_clock()

    @staticmethod
    def start_automatically_cloud_synchronization():
        AutomaticallyCloudSynchronization()

    @staticmethod
    def start_system_user_screen():
        SystemUserScreen()

    @staticmethod
    def start_system_user_clock():
        SystemUserClock()


OperationSystem()
