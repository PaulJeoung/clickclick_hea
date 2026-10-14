import json
import os

CONFIG_FILE = "mouse_config.json"

DEFAULT_CONFIG = {
    "language": "ko",
    "theme": "excel",
    "positions": [],
    "timer_hours": 10,
    "timer_minutes": 0,
    "timer_seconds": 0,
    "memo": "",
    "use_move_anim": True,
    "random_delay_pct": 0
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            cfg = DEFAULT_CONFIG.copy()
            cfg.update(data)
            return cfg
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config: dict):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception:
        pass