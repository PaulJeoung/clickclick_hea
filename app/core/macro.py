import time
import random
import pyautogui
from datetime import datetime, timedelta

class ClickMacro:
    def __init__(self, positions, stop_event, logger, options):
        self.positions = positions
        self.stop_event = stop_event
        self.logger = logger
        self.options = options

    def run(self, interval, duration):
        end_time = datetime.now() + timedelta(minutes=duration)

        while datetime.now() < end_time and not self.stop_event.is_set():
            for x, y, _ in self.positions:
                if self.stop_event.is_set():
                    return

                cur = interval
                if self.options["random"]:
                    cur *= random.uniform(0.8, 1.2)

                if self.options["animate"]:
                    pyautogui.moveTo(x, y, duration=0.2)
                else:
                    pyautogui.moveTo(x, y)

                pyautogui.click(x, y)
                self.logger.log(f"클릭: ({x}, {y})")
                time.sleep(max(0.1, cur))
