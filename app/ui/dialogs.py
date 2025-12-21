from tkinter import messagebox

def show_info(version):
    messagebox.showinfo(
        "NeoClick 정보",
        f"🖱️ 클릭클릭해 v{version}\n\n"
        "화면 보호기 방지용 매크로 프로그램\n\n"
        "F2: 위치 캡처\n"
        "F5: 시작/중지\n"
        "ESC: 종료\n\n"
        "made with python"
    )
