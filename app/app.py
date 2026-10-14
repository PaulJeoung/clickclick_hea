import tkinter as tk
from tkinter import ttk

from .ui.layout import build_ui
from .ui.styles import THEMES, apply_treeview_theme
from .ui.dialogs import show_theme_info, show_about_info, edit_interval_dialog
from .utils.logger import Logger
from .utils.config import load_config, save_config
from .utils.i18n import I18nManager
from .utils.resource import set_window_icon
from .core.macro import MacroEngine
from .core.capture import PositionCapturer
from .core.timer import MacroTimer

class ClickClickHea:
    VERSION = "2.4"

    def __init__(self):
        self.config = load_config()
        self.i18n = I18nManager(self.config.get("language", "ko"))
        self.current_theme = self.config.get("theme", "excel")
        self.positions = self.config.get("positions", [])[:5]

        self.root = tk.Tk()
        set_window_icon(self.root)
        self.style = ttk.Style()

        build_ui(self)

        self.logger = Logger(self.console)
        self.capturer = PositionCapturer(self._on_point_captured)
        self.macro = MacroEngine(
            lambda: self.positions,
            self.logger,
            self.i18n,
            self.get_macro_options
        )
        self.timer = MacroTimer(self._on_timer_tick, self._on_timer_finish)

        h = self.config.get("timer_hours", 10)
        m = self.config.get("timer_minutes", 0)
        s = self.config.get("timer_seconds", 0)
        self.timer.set_time(h, m, s)

        self.update_positions_tree()
        self.apply_theme(self.current_theme)

        # -----------------------------
        # 단축키 바인딩 (F1, F2, F5, ESC)
        # -----------------------------
        self.root.bind("<F1>", lambda e: self.show_help())
        self.root.bind("<F2>", lambda e: self.start_capture())
        self.root.bind("<F5>", lambda e: self.toggle_start_pause())
        self.root.bind("<Escape>", lambda e: self.on_close())

        self.memo_timer = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_help(self):
        """F1: 정보 표시"""
        show_about_info(self.root, self.current_theme, self.i18n, self.VERSION)

    def toggle_start_pause(self):
        """F5: 시작 / 일시정지 토글"""
        if not self.macro.is_running or self.macro.is_paused:
            self.on_start()
        else:
            self.on_pause()

    def get_macro_options(self):
        try:
            rnd = max(0, min(50, int(self.rand_spin.get())))
        except ValueError:
            rnd = 0
        return {
            "animate": self.anim_var.get(),
            "random_pct": rnd
        }

    def on_option_change(self):
        self.save()

    def on_memo_changed(self, event=None):
        if self.memo_timer:
            self.root.after_cancel(self.memo_timer)
        self.memo_timer = self.root.after(800, self.save)

    def _on_point_captured(self, x, y, btn):
        self.root.after(0, self._handle_captured_point, x, y, btn)

    def _handle_captured_point(self, x, y, btn):
        if len(self.positions) >= 5:
            show_theme_info(self.root, self.current_theme, self.i18n, "Limit", self.i18n.t("limit_reached"))
            return

        m, s, ok = edit_interval_dialog(self.root, self.current_theme, self.i18n, current_min=0, current_sec=2)
        total_interval = m * 60 + s
        if total_interval <= 0:
            total_interval = 1

        self.positions.append([x, y, btn, total_interval])
        self.update_positions_tree()
        self.save()

        btn_str = self.i18n.t(btn)
        self.logger.log(self.i18n.t("captured_done", x=x, y=y, btn=btn_str, m=m, s=s))

        show_theme_info(
            self.root, self.current_theme, self.i18n,
            self.i18n.t("popup_title_captured"),
            self.i18n.t("popup_msg_captured", x=x, y=y, btn=btn_str, m=m, s=s)
        )

    def on_tree_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return

        item_index = self.tree.index(item_id)
        if 0 <= item_index < len(self.positions):
            current_target = self.positions[item_index]
            cur_interval = current_target[3] if len(current_target) > 3 else 1
            cur_m, cur_s = cur_interval // 60, cur_interval % 60

            m, s, ok = edit_interval_dialog(self.root, self.current_theme, self.i18n, current_min=cur_m, current_sec=cur_s)
            if ok:
                new_interval = max(1, m * 60 + s)
                self.positions[item_index][3] = new_interval
                self.update_positions_tree()
                self.save()
                self.logger.log(f"#{item_index+1} 간격 변경: {m}분 {s}초")

    def update_positions_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, item in enumerate(self.positions, 1):
            x, y, btn = item[0], item[1], item[2]
            wait = item[3] if len(item) > 3 else 1
            wm, ws = wait // 60, wait % 60
            interval_str = f"{wm}m {ws}s" if wm > 0 else f"{ws}s"
            self.tree.insert("", "end", values=(idx, f"({x}, {y})", self.i18n.t(btn), interval_str))

    def clear_positions(self):
        self.positions.clear()
        self.update_positions_tree()
        self.save()

    def start_capture(self):
        if len(self.positions) >= 5:
            show_theme_info(self.root, self.current_theme, self.i18n, "Limit", self.i18n.t("limit_reached"))
            return
        self.logger.log(self.i18n.t("capturing_msg"))
        self.capturer.start()

    def apply_custom_timer(self):
        try:
            h = int(self.h_spin.get())
            m = int(self.m_spin.get())
            s = int(self.s_spin.get())
            self.timer.set_time(h, m, s)
            self.config["timer_hours"] = h
            self.config["timer_minutes"] = m
            self.config["timer_seconds"] = s
            self.save()
            self.logger.log(f"타이머 설정 적용: {h:02d}:{m:02d}:{s:02d}")
        except ValueError:
            pass

    def draw_bar_gauge(self, percent):
        canvas = self.bar_canvas
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 10:
            w = 340
        if h < 5:
            h = 8

        th = THEMES.get(self.current_theme, THEMES["excel"])
        bg_col = th.get("progress_bg", "#e0e0e0")
        fill_col = th.get("progress_fill", "#0f9d58")

        canvas.create_rectangle(0, 0, w, h, fill=bg_col, outline="")
        fill_w = max(0, int((percent / 100.0) * w))
        if fill_w > 0:
            canvas.create_rectangle(0, 0, fill_w, h, fill=fill_col, outline="")

    def _on_timer_tick(self, remaining_sec, total_sec):
        def _update():
            hrs = remaining_sec // 3600
            mins = (remaining_sec % 3600) // 60
            secs = remaining_sec % 60
            self.clock_label.config(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")
            pct = (remaining_sec / total_sec) * 100 if total_sec > 0 else 0
            self.draw_bar_gauge(pct)
        self.root.after(0, _update)

    def _on_timer_finish(self):
        def _finish():
            self.macro.stop()
            self.status_label.config(text=self.i18n.t("finished"))
            self.logger.log(self.i18n.t("finished"))
            self.draw_bar_gauge(0)
        self.root.after(0, _finish)

    def on_start(self):
        if not self.positions:
            show_theme_info(self.root, self.current_theme, self.i18n, "Notice", self.i18n.t("need_coords"))
            return

        formatted_time = self.clock_label.cget("text")
        if self.macro.is_paused:
            self.logger.log(self.i18n.t("macro_resume"))
        else:
            self.logger.log(self.i18n.t("macro_start", time=formatted_time))

        self.status_label.config(text=self.i18n.t("running"))
        self.macro.start()
        self.timer.start()

    def on_pause(self):
        if self.macro.is_running and not self.macro.is_paused:
            self.macro.pause()
            self.timer.pause()
            self.status_label.config(text=self.i18n.t("paused"))
            self.logger.log(self.i18n.t("macro_pause"))

    def on_stop(self):
        self.macro.stop()
        self.timer.stop_and_reset()
        self.status_label.config(text=self.i18n.t("stopped"))
        self.logger.log(self.i18n.t("macro_stop"))

    def on_lang_change(self, event=None):
        selected_lang = self.lang_combo.get()
        self.i18n.set_language(selected_lang)
        self.config["language"] = selected_lang
        self.save()
        self.refresh_text()

    def refresh_text(self):
        self.root.title(self.i18n.t("title"))
        self.theme_lbl.config(text=self.i18n.t("theme") + ":")
        self.lang_lbl.config(text=self.i18n.t("language") + ":")
        self.coord_frame.config(text=self.i18n.t("coord_section"))
        self.capture_btn.config(text=self.i18n.t("capture_btn"))
        self.clear_btn.config(text=self.i18n.t("clear_coords"))
        self.tree.heading("idx", text="#")
        self.tree.heading("pos", text=self.i18n.t("col_pos"))
        self.tree.heading("btn", text=self.i18n.t("col_btn"))
        self.tree.heading("interval", text=self.i18n.t("col_interval"))
        self.anim_chk.config(text=self.i18n.t("move_anim"))
        self.rand_lbl.config(text=self.i18n.t("random_delay"))
        self.timer_frame.config(text=self.i18n.t("timer_section"))
        self.h_lbl.config(text=self.i18n.t("hours"))
        self.m_lbl.config(text=self.i18n.t("minutes"))
        self.s_lbl.config(text=self.i18n.t("seconds"))
        self.apply_timer_btn.config(text=self.i18n.t("apply_timer"))
        self.status_label.config(text=self.i18n.t("ready"))
        self.log_frame.config(text=self.i18n.t("realtime_log"))
        self.memo_frame.config(text=self.i18n.t("temp_memo"))
        self.update_positions_tree()
        self.apply_theme(self.current_theme)

    def on_theme_change(self, event=None):
        self.current_theme = self.theme_combo.get()
        self.config["theme"] = self.current_theme
        self.save()
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme_key):
        th = THEMES.get(theme_key, THEMES["excel"])
        ff = th["font_family"]

        apply_treeview_theme(self.style, th)

        if th["is_terminal"]:
            self.theme_banner.config(
                text="PS C:\\Admin\\ClickClickHea> _",
                bg=th["header_bg"], fg=th["header_fg"], font=(ff, 8, "bold")
            )
            start_txt = "[ RUN ]"
            pause_txt = "[ WAIT ]"
            stop_txt  = "[ RESET ]"
        elif th["is_kids"]:
            self.theme_banner.config(
                text="🎀 곰돌이와 함께하는 톡톡 매크로! 🧸✨",
                bg=th["header_bg"], fg=th["header_fg"], font=(ff, 8, "bold")
            )
            start_txt = "▶ 톡톡 시작! 🎮"
            pause_txt = "⏸ 멈칫! 🐰"
            stop_txt  = "⏹ 처음으로! 🍭"
        else:
            self.theme_banner.config(
                text="fx  =SUM(CLICK_TARGETS!A1:D5)  [AutoSheet Macro]",
                bg=th["card_bg"], fg=th["accent"], font=(ff, 8, "italic"), relief="solid", bd=1
            )
            start_txt = "▶ " + self.i18n.t("start")
            pause_txt = "⏸ " + self.i18n.t("pause")
            stop_txt  = "⏹ " + self.i18n.t("stop")

        self.start_btn.config(text=start_txt)
        self.pause_btn.config(text=pause_txt)
        self.stop_btn.config(text=stop_txt)

        self.root.configure(bg=th["bg"])
        self.main_frame.configure(bg=th["bg"])
        self.top_bar.configure(bg=th["bg"])
        self.theme_lbl.configure(bg=th["bg"], fg=th["text"], font=(ff, 8))
        self.lang_lbl.configure(bg=th["bg"], fg=th["text"], font=(ff, 8))

        self.coord_frame.configure(bg=th["card_bg"], fg=th["fg"], font=(ff, 8, "bold"))
        self.capture_btn.configure(bg=th["btn_normal"], fg=th["btn_normal_fg"], font=(ff, 8, "bold"), relief="groove")
        self.clear_btn.configure(bg=th["btn_normal"], fg=th["btn_normal_fg"], font=(ff, 8), relief="groove")

        self.opt_frame.configure(bg=th["bg"])
        self.anim_chk.configure(bg=th["bg"], fg=th["text"], selectcolor=th["card_bg"], font=(ff, 8))

        self.timer_frame.configure(bg=th["card_bg"], fg=th["fg"], font=(ff, 8, "bold"))
        self.clock_label.configure(bg=th["card_bg"], fg=th["fg"], font=(ff, 13, "bold"))
        self.status_label.configure(bg=th["card_bg"], fg=th["text"], font=(ff, 8))
        self.h_lbl.configure(bg=th["card_bg"], fg=th["text"])
        self.m_lbl.configure(bg=th["card_bg"], fg=th["text"])
        self.s_lbl.configure(bg=th["card_bg"], fg=th["text"])
        self.apply_timer_btn.configure(bg=th["btn_normal"], fg=th["btn_normal_fg"], relief="groove")

        self.bar_canvas.configure(bg=th["progress_bg"])
        self.draw_bar_gauge(100)

        self.action_box.configure(bg=th["bg"])
        self.start_btn.configure(bg=th["btn_start"], fg=th["btn_text"], font=(ff, 8, "bold"), relief="flat")
        self.pause_btn.configure(bg=th["btn_pause"], fg=th["btn_text"], font=(ff, 8, "bold"), relief="flat")
        self.stop_btn.configure(bg=th["btn_stop"], fg=th["btn_text"], font=(ff, 8, "bold"), relief="flat")

        self.log_frame.configure(bg=th["card_bg"], fg=th["fg"], font=(ff, 8, "bold"))
        self.console.configure(bg=th["console_bg"], fg=th["console_fg"], insertbackground=th["console_fg"])

        self.memo_frame.configure(bg=th["card_bg"], fg=th["fg"], font=(ff, 8, "bold"))
        self.memo_text.configure(bg=th["memo_bg"], fg=th["memo_fg"], insertbackground=th["memo_fg"])

    def save(self):
        try:
            rnd = int(self.rand_spin.get())
        except (ValueError, AttributeError):
            rnd = 0
        save_config({
            "language": self.i18n.lang,
            "theme": self.current_theme,
            "positions": self.positions,
            "timer_hours": int(self.h_spin.get()),
            "timer_minutes": int(self.m_spin.get()),
            "timer_seconds": int(self.s_spin.get()),
            "memo": self.memo_text.get("1.0", "end-1c"),
            "use_move_anim": self.anim_var.get(),
            "random_delay_pct": rnd
        })

    def on_close(self):
        self.macro.stop()
        self.capturer.stop()
        self.save()
        self.root.destroy()

    def run(self):
        self.root.mainloop()