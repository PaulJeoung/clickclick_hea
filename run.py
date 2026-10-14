# run.py
import pyautogui
from app.app import ClickClickHea

pyautogui.FAILSAFE = False

def main():
    app = ClickClickHea()
    app.run()

if __name__ == "__main__":
    main()