from tkinter import ttk

THEMES = {
    "excel": {
        "key": "excel",
        "bg": "#f8f9fa",
        "card_bg": "#ffffff",
        "header_bg": "#0f9d58",
        "header_fg": "#ffffff",
        "fg": "#0f9d58",
        "text": "#202124",
        "text_secondary": "#5f6368",
        "border": "#dadce0",
        "accent": "#0f9d58",
        "btn_start": "#0f9d58",
        "btn_pause": "#f4b400",
        "btn_stop": "#d93025",
        "btn_normal": "#ffffff",
        "btn_normal_fg": "#3c4043",
        "btn_text": "#ffffff",
        "progress_bg": "#e8eaed",
        "progress_fill": "#0f9d58",
        "console_bg": "#ffffff",
        "console_fg": "#202124",
        "memo_bg": "#fffde7",           # 포스트잇 느낌의 옅은 노랑
        "memo_fg": "#333333",
        "tree_bg": "#ffffff",
        "tree_fg": "#202124",
        "tree_selected": "#e8f0fe",
        "font_family": "Segoe UI",
        "font_size": 8,
        "is_kids": False,
        "is_terminal": False
    },
    "terminal": {
        "key": "terminal",
        "bg": "#0c0c0c",
        "card_bg": "#141414",
        "header_bg": "#012456",
        "header_fg": "#ffffff",
        "fg": "#00ff66",
        "text": "#00ff66",
        "text_secondary": "#767676",
        "border": "#00ff66",
        "accent": "#00ff66",
        "btn_start": "#004d20",
        "btn_pause": "#4d3d00",
        "btn_stop": "#4d0000",
        "btn_normal": "#1e1e1e",
        "btn_normal_fg": "#00ff66",
        "btn_text": "#00ff66",
        "progress_bg": "#1e1e1e",
        "progress_fill": "#00ff66",
        "console_bg": "#000000",
        "console_fg": "#00ff66",
        "memo_bg": "#121212",
        "memo_fg": "#00ff66",
        "tree_bg": "#000000",           # 터미널용 블랙 배경
        "tree_fg": "#00ff66",           # 터미널용 네온 텍스트
        "tree_selected": "#003b15",
        "font_family": "Consolas",
        "font_size": 8,
        "is_kids": False,
        "is_terminal": True
    },
    "kids": {
        "key": "kids",
        "bg": "#fff5f8",
        "card_bg": "#ffffff",
        "header_bg": "#ff7597",
        "header_fg": "#ffffff",
        "fg": "#ff4d6d",
        "text": "#594a4e",
        "text_secondary": "#9e8e93",
        "border": "#ffccd5",
        "accent": "#ff7597",
        "btn_start": "#ff7597",
        "btn_pause": "#ffb703",
        "btn_stop": "#ff4d6d",
        "btn_normal": "#ffe5ec",
        "btn_normal_fg": "#c9184a",
        "btn_text": "#ffffff",
        "progress_bg": "#ffe5ec",
        "progress_fill": "#ff7597",
        "console_bg": "#fffbfc",
        "console_fg": "#594a4e",
        "memo_bg": "#fff0f3",
        "memo_fg": "#594a4e",
        "tree_bg": "#ffffff",
        "tree_fg": "#594a4e",
        "tree_selected": "#ffccd5",
        "font_family": "Malgun Gothic",
        "font_size": 8,
        "is_kids": True,
        "is_terminal": False
    }
}

def apply_treeview_theme(style: ttk.Style, th: dict):
    style.theme_use("clam")
    style.configure(
        "Custom.Treeview",
        background=th["tree_bg"],
        foreground=th["tree_fg"],
        fieldbackground=th["tree_bg"],
        font=(th["font_family"], 8),
        borderwidth=0
    )
    style.map(
        "Custom.Treeview",
        background=[("selected", th["tree_selected"])],
        foreground=[("selected", th["fg"])]
    )
    style.configure(
        "Custom.Treeview.Heading",
        background=th["card_bg"],
        foreground=th["fg"],
        font=(th["font_family"], 8, "bold")
    )