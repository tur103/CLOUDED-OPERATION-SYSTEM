import threading
import subprocess
from constants import *


class SystemUserNotes(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        subprocess.call(" ".join([PYTHON, NOTES_PROGRAM]))
