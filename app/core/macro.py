import time
import random
import threading
import pyautogui

class MacroEngine:
    def __init__(self, get_positions, logger, i18n, options_provider):
        self.get_positions = get_positions
        self.logger = logger
        self.i18n = i18n
        self.options_provider = options_provider  # {"animate": bool, "random_pct": int}
        self.is_running = False
        self.is_paused = False
        self.stop_requested = False
        self.thread = None

    def start(self):
        if self.is_running and self.is_paused:
            self.is_paused = False
            return

        self.is_running = True
        self.is_paused = False
        self.stop_requested = False
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def pause(self):
        self.is_paused = True

    def stop(self):
        self.stop_requested = True
        self.is_running = False
        self.is_paused = False

    def _loop(self):
        while self.is_running and not self.stop_requested:
            while self.is_paused and not self.stop_requested:
                time.sleep(0.2)

            if self.stop_requested:
                break

            positions = self.get_positions()
            opts = self.options_provider()
            use_anim = opts.get("animate", True)
            random_pct = opts.get("random_pct", 0)

            for x, y, btn, base_wait in positions:
                if not self.is_running or self.stop_requested or self.is_paused:
                    break

                try:
                    # 1. 마우스 이동 애니메이션 옵션 적용
                    if use_anim:
                        pyautogui.moveTo(x, y, duration=0.25)
                    else:
                        pyautogui.moveTo(x, y)

                    pyautogui.click(x=x, y=y, button=btn)
                    btn_label = self.i18n.t(btn)

                    # 2. 랜덤 딜레이 계산 (최대 1~50% 편차)
                    actual_wait = float(base_wait)
                    if random_pct > 0:
                        variation = random.uniform(-random_pct, random_pct) / 100.0
                        actual_wait = max(0.1, actual_wait * (1.0 + variation))

                    self.logger.log(
                        self.i18n.t("click_log", x=x, y=y, btn=btn_label, wait=f"{actual_wait:.1f}")
                    )
                except Exception as e:
                    self.logger.log(f"Error: {e}")

                # 세분화된 슬립 처리 (즉시 멈춤 대응)
                steps = int(max(0.1, actual_wait) * 10)
                for _ in range(steps):
                    if self.stop_requested or self.is_paused:
                        break
                    time.sleep(0.1)

            time.sleep(0.05)