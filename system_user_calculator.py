import threading
import subprocess
from constants import *


class SystemUserCalculator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        subprocess.call(" ".join([PYTHON, os.path.join(MAIN_FOLDER, CALCULATOR_PROGRAM)]))
