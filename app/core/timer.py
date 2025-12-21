import time
from datetime import datetime

def run_timer(app):
    while app.is_running and not app.stop_event.is_set():
        remain = app.end_time - datetime.now()
        app.timer_label.config(text=f"남은 시간: {str(remain).split('.')[0]}")
        time.sleep(0.5)
