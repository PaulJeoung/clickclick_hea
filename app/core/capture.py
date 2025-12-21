import pyautogui
from tkinter import messagebox

def capture_position(root, logger, positions, update_ui):
    root.withdraw()
    messagebox.showinfo("위치 캡처", "원하는 위치를 클릭하세요.")
    x, y = pyautogui.position()
    positions.append((x, y, "왼쪽"))
    logger.log(f"위치 저장: ({x}, {y})")
    update_ui()
    root.deiconify()
