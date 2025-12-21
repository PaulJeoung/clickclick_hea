import tkinter as tk
import threading
from ui.layout import build_ui
from ui.styles import setup_styles
from utils.logger import Logger
from utils.config import load_config, save_config
from core.macro import ClickMacro
from core.capture import capture_position

class NeoCyberClickMacro:
    VERSION = "1.3"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("클릭클릭해 v1.3")
        self.root.geometry("400x500")

        setup_styles()
        build_ui(self)

        self.logger = Logger(self.console)
        self.stop_event = threading.Event()
        self.is_running = False
        self.positions = []

        self.load()

        self.root.bind("<F2>", lambda e: self.capture())
        self.root.bind("<Escape>", lambda e: self.exit())

    def capture(self):
        capture_position(self.root, self.logger, self.positions, lambda: None)
        self.save()

    def start_macro(self):
        if self.is_running or not self.positions:
            return

        self.is_running = True
        self.stop_event.clear()

        macro = ClickMacro(
            self.positions,
            self.stop_event,
            self.logger,
            {"random": True, "animate": True}
        )

        threading.Thread(
            target=macro.run,
            args=(10, 60),
            daemon=True
        ).start()

    def stop_macro(self):
        self.stop_event.set()
        self.is_running = False

    def save(self):
        save_config({"positions": self.positions})

    def load(self):
        data = load_config()
        self.positions = data.get("positions", [])

    def exit(self):
        self.save()
        self.root.destroy()

    def run(self):
        self.logger.log("프로그램 시작")
        self.root.mainloop()
