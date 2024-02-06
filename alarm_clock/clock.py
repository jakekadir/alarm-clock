import os
from pathlib import Path
from time import time

ALARM_RINGING_VAR_NAME = "ALARM_CLOCK_RINGING"


def set_ringing_state(func):
    def inner(*args, **kwargs):
        os.environ[ALARM_RINGING_VAR_NAME] = "1"
        ret_val = func(*args, **kwargs)
        os.environ[ALARM_RINGING_VAR_NAME] = "0"
        return ret_val

    return inner


class Clock:
    def __init__(self, filename: Path = Path("alarm.mp3"), ring_duration: int = 300):
        # audio file
        self.filename = filename
        self.ring_duration = ring_duration

    def should_ring(self) -> int:
        return int(os.environ[ALARM_RINGING_VAR_NAME])

    @set_ringing_state
    def ring(self):
        start_time = time()
        # keep ringing for given duration,
        # or until env var is switched to 0
        while (time() - start_time < self.ring_duration) and self.should_ring():
            self.play()

    def play(self):
        # emits a noise (blocking)
        os.system("mpg123 " + str(self.filename))
