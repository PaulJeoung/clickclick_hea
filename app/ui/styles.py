from tkinter import ttk

COLORS = {
    'bg': '#0f111a',
    'frame_bg': '#1a1c25',
    'accent': '#00e676',
    'accent_alt': '#00b0ff',
    'text': '#eceff1',
    'text_secondary': '#b0bec5',
    'error': '#ff5252',
    'warning': '#ffab40',
}

def setup_styles():
    style = ttk.Style()
    style.configure('Neo.TFrame', background=COLORS['frame_bg'])
    style.configure('Neo.TButton', background=COLORS['accent'])
    style.configure(
        'Neo.Horizontal.TProgressbar',
        background=COLORS['accent'],
        troughcolor=COLORS['frame_bg']
    )
