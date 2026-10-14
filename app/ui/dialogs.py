import tkinter as tk
from ..utils.resource import set_window_icon
from .styles import THEMES

class CustomThemeDialog(tk.Toplevel):
    def __init__(self, parent, theme_key, title):
        super().__init__(parent)
        self.title(title)
        self.theme = THEMES.get(theme_key, THEMES["excel"])
        set_window_icon(self)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(bg=self.theme["bg"])

def show_theme_info(parent, theme_key, i18n, title, message):
    dialog = CustomThemeDialog(parent, theme_key, title)
    dialog.geometry("340x190")
    th = dialog.theme

    header_title = "🖱️ " + title
    if th["is_kids"]:
        header_title = "🎀✨ " + title + " ✨🎀"
    elif th["is_terminal"]:
        header_title = "[INFO] :: " + title

    hdr = tk.Label(dialog, text=header_title, bg=th["header_bg"], fg=th["header_fg"], font=(th["font_family"], 9, "bold"), pady=4)
    hdr.pack(fill="x")

    body = tk.Label(dialog, text=message, bg=th["card_bg"], fg=th["text"], font=(th["font_family"], 9), justify="center", padx=10, pady=10)
    body.pack(fill="both", expand=True, padx=10, pady=(8, 4))

    btn = tk.Button(
        dialog, text=i18n.t("confirm"), bg=th["btn_start"], fg=th["btn_text"],
        font=(th["font_family"], 9, "bold"), width=12, relief="flat", command=dialog.destroy
    )
    btn.pack(pady=(0, 10))
    parent.wait_window(dialog)

def show_about_info(parent, theme_key, i18n, version):
    """F1 단축키용 정보 안내 다이얼로그"""
    info_text = (
        f"🖱️ 클릭클릭해 (ClickClickHea) v{version}\n\n"
        "[ 단축키 안내 ]\n"
        "• F1  : 단축키 및 프로그램 정보\n"
        "• F2  : 마우스 좌표 캡처 시작\n"
        "• F5  : 매크로 시작 / 일시정지\n"
        "• ESC : 프로그램 안전 종료\n"
    )
    show_theme_info(parent, theme_key, i18n, "프로그램 정보", info_text)

def edit_interval_dialog(parent, theme_key, i18n, current_min=0, current_sec=2):
    dialog = CustomThemeDialog(parent, theme_key, i18n.t("interval_dialog_title"))
    dialog.geometry("300x170")
    th = dialog.theme

    title_txt = i18n.t("interval_dialog_title")
    if th["is_kids"]:
        title_txt = "⏳🍓 " + title_txt
    elif th["is_terminal"]:
        title_txt = "[CONFIG] >> " + title_txt

    hdr = tk.Label(dialog, text=title_txt, bg=th["header_bg"], fg=th["header_fg"], font=(th["font_family"], 9, "bold"), pady=4)
    hdr.pack(fill="x")

    lbl = tk.Label(dialog, text=i18n.t("interval_dialog_desc"), bg=th["bg"], fg=th["text"], font=(th["font_family"], 9))
    lbl.pack(pady=(8, 4))

    row = tk.Frame(dialog, bg=th["bg"])
    row.pack(pady=4)

    m_spin = tk.Spinbox(row, from_=0, to=59, width=4, justify="center", font=(th["font_family"], 10))
    m_spin.delete(0, "end")
    m_spin.insert(0, str(current_min))
    m_spin.pack(side="left")
    tk.Label(row, text=i18n.t("minutes"), bg=th["bg"], fg=th["text"], font=(th["font_family"], 9)).pack(side="left", padx=(2, 8))

    s_spin = tk.Spinbox(row, from_=0, to=59, width=4, justify="center", font=(th["font_family"], 10))
    s_spin.delete(0, "end")
    s_spin.insert(0, str(current_sec))
    s_spin.pack(side="left")
    tk.Label(row, text=i18n.t("seconds"), bg=th["bg"], fg=th["text"], font=(th["font_family"], 9)).pack(side="left", padx=(2, 0))

    result = {"min": current_min, "sec": current_sec, "ok": False}

    def on_ok():
        try:
            result["min"] = max(0, int(m_spin.get()))
            result["sec"] = max(0, int(s_spin.get()))
            result["ok"] = True
        except ValueError:
            pass
        dialog.destroy()

    btn_row = tk.Frame(dialog, bg=th["bg"])
    btn_row.pack(pady=10)

    btn_ok = tk.Button(btn_row, text=i18n.t("confirm"), bg=th["btn_start"], fg=th["btn_text"], font=(th["font_family"], 9, "bold"), width=8, relief="flat", command=on_ok)
    btn_ok.pack(side="left", padx=4)

    btn_cancel = tk.Button(btn_row, text=i18n.t("cancel"), bg=th["btn_normal"], fg=th["btn_normal_fg"], font=(th["font_family"], 9), width=8, relief="flat", command=dialog.destroy)
    btn_cancel.pack(side="left", padx=4)

    parent.wait_window(dialog)
    return result["min"], result["sec"], result["ok"]