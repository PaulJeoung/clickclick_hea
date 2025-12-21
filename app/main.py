import pyautogui
from app.app import NeoCyberClickMacro

pyautogui.FAILSAFE = True

def main():
    app = NeoCyberClickMacro()
    app.run()

if __name__ == "__main__":
    main()
