import tkinter as tk
from datetime import datetime

class Logger:
    def __init__(self, text_widget: tk.Text):
        self.widget = text_widget

    def log(self, message: str):
        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        formatted = f"{timestamp}{message}\n"
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, formatted)
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")