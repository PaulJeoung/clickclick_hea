import time
import threading

class MacroTimer:
    def __init__(self, on_tick, on_finish):
        self.total_seconds = 10 * 3600  # Default 10 hours
        self.remaining_seconds = self.total_seconds
        self.is_running = False
        self.is_paused = False
        self.stop_requested = False
        self.on_tick = on_tick
        self.on_finish = on_finish
        self.thread = None

    def set_time(self, hours, minutes, seconds):
        total = hours * 3600 + minutes * 60 + seconds
        self.total_seconds = max(1, min(24 * 3600, total))
        self.remaining_seconds = self.total_seconds
        self.on_tick(self.remaining_seconds, self.total_seconds)

    def start(self):
        if self.is_running and self.is_paused:
            self.is_paused = False
            return

        self.is_running = True
        self.is_paused = False
        self.stop_requested = False
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def pause(self):
        self.is_paused = True

    def stop_and_reset(self):
        self.stop_requested = True
        self.is_running = False
        self.is_paused = False
        self.remaining_seconds = self.total_seconds
        self.on_tick(self.remaining_seconds, self.total_seconds)

    def _run(self):
        while self.remaining_seconds > 0 and not self.stop_requested:
            if not self.is_paused:
                time.sleep(1)
                if not self.is_paused and not self.stop_requested:
                    self.remaining_seconds -= 1
                    self.on_tick(self.remaining_seconds, self.total_seconds)
            else:
                time.sleep(0.2)

        if self.remaining_seconds <= 0 and not self.stop_requested:
            self.is_running = False
            self.on_finish()