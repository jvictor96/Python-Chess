import time
from machine_core import MovementStateHandler

class OpponentListener(MovementStateHandler):
    def __call__(self, msg):
        while True:
            time.wait(1)