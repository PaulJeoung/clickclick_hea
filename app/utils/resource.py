import sys
import os

def get_resource_path(relative_path: str) -> str:
    """PyInstaller 및 로컬 실행 환경 모두 지원"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        # app/utils/resource.py 기준 상위 2단계가 루트
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
    return os.path.join(base_path, relative_path)

def set_window_icon(window):
    """윈도우 및 다이얼로그에 mouse.ico 적용 (Tkinter 기본 깃털 제거)"""
    icon_path = get_resource_path(os.path.join("assets", "mouse.ico"))
    if os.path.exists(icon_path):
        try:
            window.iconbitmap(icon_path)
        except Exception:
            pass