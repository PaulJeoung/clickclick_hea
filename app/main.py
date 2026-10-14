import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pyautogui
from app import ClickClickHea

pyautogui.FAILSAFE = False

def main():
    app = ClickClickHea()
    app.run()

if __name__ == "__main__":
    main()