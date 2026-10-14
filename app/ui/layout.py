import tkinter as tk
from tkinter import ttk
from .styles import THEMES

def build_ui(app):
    root = app.root
    root.title(app.i18n.t("title"))
    
    # 세로 여백을 없앤 컴팩트 핏 (380x560, 최소 360x540)
    root.geometry("300x500")
    # root.minsize(360, 400)

    # main_frame이 불필요하게 아래로 늘어나지 않도록 설정
    app.main_frame = tk.Frame(root)
    app.main_frame.pack(fill="both", expand=True, padx=6, pady=4)

    # 1. 헤더 배너
    app.theme_banner = tk.Label(app.main_frame, text="", anchor="w", padx=6, pady=2)
    app.theme_banner.pack(fill="x", pady=(0, 2))

    # 2. Top Bar (테마 / 언어)
    app.top_bar = tk.Frame(app.main_frame)
    app.top_bar.pack(fill="x", pady=(0, 2))

    app.theme_lbl = tk.Label(app.top_bar, text=app.i18n.t("theme") + ":")
    app.theme_lbl.pack(side="left")
    app.theme_combo = ttk.Combobox(app.top_bar, state="readonly", width=8, values=["excel", "terminal", "kids"])
    app.theme_combo.set(app.current_theme)
    app.theme_combo.pack(side="left", padx=(2, 6))
    app.theme_combo.bind("<<ComboboxSelected>>", app.on_theme_change)

    app.lang_lbl = tk.Label(app.top_bar, text=app.i18n.t("language") + ":")
    app.lang_lbl.pack(side="left")
    app.lang_combo = ttk.Combobox(app.top_bar, state="readonly", width=5, values=["ko", "en", "zh", "es"])
    app.lang_combo.set(app.i18n.lang)
    app.lang_combo.pack(side="left", padx=(2, 0))
    app.lang_combo.bind("<<ComboboxSelected>>", app.on_lang_change)

    # 3. 좌표 목록 (더블클릭 간격수정 지원)
    app.coord_frame = tk.LabelFrame(app.main_frame, text=app.i18n.t("coord_section"), padx=4, pady=2)
    app.coord_frame.pack(fill="x", pady=2)

    btn_row = tk.Frame(app.coord_frame)
    btn_row.pack(fill="x", pady=(0, 2))
    app.capture_btn = tk.Button(btn_row, text=app.i18n.t("capture_btn"), command=app.start_capture)
    app.capture_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
    app.clear_btn = tk.Button(btn_row, text=app.i18n.t("clear_coords"), command=app.clear_positions)
    app.clear_btn.pack(side="right")

    cols = ("idx", "pos", "btn", "interval")
    app.tree = ttk.Treeview(app.coord_frame, columns=cols, show="headings", height=4, style="Custom.Treeview")
    app.tree.heading("idx", text="#")
    app.tree.heading("pos", text=app.i18n.t("col_pos"))
    app.tree.heading("btn", text=app.i18n.t("col_btn"))
    app.tree.heading("interval", text=app.i18n.t("col_interval"))
    app.tree.column("idx", width=25, anchor="center")
    app.tree.column("pos", width=110, anchor="center")
    app.tree.column("btn", width=65, anchor="center")
    app.tree.column("interval", width=85, anchor="center")
    app.tree.pack(fill="x")
    app.tree.bind("<Double-1>", app.on_tree_double_click)

    # 4. 부가 옵션 (이동 애니메이션 & 랜덤 딜레이)
    app.opt_frame = tk.Frame(app.main_frame)
    app.opt_frame.pack(fill="x", pady=2)

    app.anim_var = tk.BooleanVar(value=app.config.get("use_move_anim", True))
    app.anim_chk = tk.Checkbutton(
        app.opt_frame, 
        text=app.i18n.t("move_anim"), 
        variable=app.anim_var, 
        command=app.on_option_change
    )
    app.anim_chk.pack(side="left")

    rand_box = tk.Frame(app.opt_frame)
    rand_box.pack(side="right")
    
    app.rand_lbl = tk.Label(rand_box, text=app.i18n.t("random_delay"), font=("Segoe UI", 8))
    app.rand_lbl.pack(side="left")
    
    app.rand_spin = tk.Spinbox(rand_box, from_=0, to=50, width=3, justify="center")
    app.rand_spin.delete(0, "end")
    app.rand_spin.insert(0, str(app.config.get("random_delay_pct", 0)))
    app.rand_spin.pack(side="left")
    tk.Label(rand_box, text="%", font=("Segoe UI", 8)).pack(side="left")
    app.rand_spin.bind("<FocusOut>", lambda e: app.on_option_change())
    app.rand_spin.bind("<Return>", lambda e: app.on_option_change())

    # 5. 타이머 & 모던 바 프로그레스
    app.timer_frame = tk.LabelFrame(app.main_frame, text=app.i18n.t("timer_section"), padx=4, pady=2)
    app.timer_frame.pack(fill="x", pady=2)

    time_row = tk.Frame(app.timer_frame)
    time_row.pack(pady=1)

    app.h_spin = tk.Spinbox(time_row, from_=0, to=24, width=3, justify="center")
    app.h_spin.delete(0, "end")
    app.h_spin.insert(0, str(app.config.get("timer_hours", 10)))
    app.h_spin.pack(side="left")
    app.h_lbl = tk.Label(time_row, text=app.i18n.t("hours"), font=("Segoe UI", 8))
    app.h_lbl.pack(side="left", padx=(1, 3))

    app.m_spin = tk.Spinbox(time_row, from_=0, to=59, width=3, justify="center")
    app.m_spin.delete(0, "end")
    app.m_spin.insert(0, str(app.config.get("timer_minutes", 0)))
    app.m_spin.pack(side="left")
    app.m_lbl = tk.Label(time_row, text=app.i18n.t("minutes"), font=("Segoe UI", 8))
    app.m_lbl.pack(side="left", padx=(1, 3))

    app.s_spin = tk.Spinbox(time_row, from_=0, to=59, width=3, justify="center")
    app.s_spin.delete(0, "end")
    app.s_spin.insert(0, str(app.config.get("timer_seconds", 0)))
    app.s_spin.pack(side="left")
    app.s_lbl = tk.Label(time_row, text=app.i18n.t("seconds"), font=("Segoe UI", 8))
    app.s_lbl.pack(side="left", padx=(1, 4))

    app.apply_timer_btn = tk.Button(time_row, text=app.i18n.t("apply_timer"), font=("Segoe UI", 8), command=app.apply_custom_timer)
    app.apply_timer_btn.pack(side="left")

    clock_box = tk.Frame(app.timer_frame)
    clock_box.pack(fill="x", pady=1)
    app.clock_label = tk.Label(clock_box, text="10:00:00", font=("Helvetica", 13, "bold"))
    app.clock_label.pack(side="left")
    app.status_label = tk.Label(clock_box, text=app.i18n.t("ready"), font=("Segoe UI", 8))
    app.status_label.pack(side="right")

    app.bar_canvas = tk.Canvas(app.timer_frame, height=8, highlightthickness=0)
    app.bar_canvas.pack(fill="x", pady=(1, 1))

    # 6. 액션 버튼 (시작 / 일시정지 / 정지)
    action_box = tk.Frame(app.main_frame)
    action_box.pack(fill="x", pady=2)
    app.action_box = action_box

    app.start_btn = tk.Button(action_box, text=app.i18n.t("start"), command=app.on_start)
    app.start_btn.pack(side="left", fill="x", expand=True, padx=2)

    app.pause_btn = tk.Button(action_box, text=app.i18n.t("pause"), command=app.on_pause)
    app.pause_btn.pack(side="left", fill="x", expand=True, padx=2)

    app.stop_btn = tk.Button(action_box, text=app.i18n.t("stop"), command=app.on_stop)
    app.stop_btn.pack(side="left", fill="x", expand=True, padx=2)

    # 7. 축소된 실시간 로그 (스크롤바 포함, 높이 3)
    app.log_frame = tk.LabelFrame(app.main_frame, text=app.i18n.t("realtime_log"), padx=2, pady=2)
    app.log_frame.pack(fill="x", pady=2)

    log_box = tk.Frame(app.log_frame)
    log_box.pack(fill="x", expand=False)

    app.console = tk.Text(log_box, height=3, wrap="word", state="disabled", font=("Consolas", 8))
    app.log_scroll = tk.Scrollbar(log_box, command=app.console.yview)
    app.console.configure(yscrollcommand=app.log_scroll.set)

    app.console.pack(side="left", fill="both", expand=True)
    app.log_scroll.pack(side="right", fill="y")

    # 8. 임시 메모장 (자동 저장)
    app.memo_frame = tk.LabelFrame(app.main_frame, text=app.i18n.t("temp_memo"), padx=2, pady=2)
    app.memo_frame.pack(fill="x", pady=(2, 2))

    memo_box = tk.Frame(app.memo_frame)
    memo_box.pack(fill="x", expand=False)

    app.memo_text = tk.Text(memo_box, height=3, wrap="word", font=("Segoe UI", 8))
    app.memo_scroll = tk.Scrollbar(memo_box, command=app.memo_text.yview)
    app.memo_text.configure(yscrollcommand=app.memo_scroll.set)

    app.memo_text.pack(side="left", fill="both", expand=True)
    app.memo_scroll.pack(side="right", fill="y")

    app.memo_text.insert("1.0", app.config.get("memo", ""))
    app.memo_text.bind("<KeyRelease>", app.on_memo_changed)