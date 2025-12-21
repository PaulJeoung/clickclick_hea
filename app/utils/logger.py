from datetime import datetime
import tkinter as tk

class Logger:
    def __init__(self, text_widget: tk.Text):
        self.console = text_widget

    def log(self, message: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self.console.insert(tk.END, f"[{ts}] {message}\n")
        self.console.see(tk.END)
