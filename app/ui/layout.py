import tkinter as tk
from tkinter import ttk
from ui.styles import COLORS

def build_ui(app):
    root = app.root

    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    app.run_btn = tk.Button(
        frame, text="▶ START", bg=COLORS["accent"],
        command=app.start_macro
    )
    app.run_btn.pack(fill="x", pady=5)

    app.pause_btn = tk.Button(
        frame, text="⏸ STOP", bg=COLORS["warning"],
        command=app.stop_macro
    )
    app.pause_btn.pack(fill="x", pady=5)

    app.timer_label = tk.Label(frame, text="READY")
    app.timer_label.pack(pady=5)

    app.console = tk.Text(frame, height=6)
    app.console.pack(fill="both", expand=True)
