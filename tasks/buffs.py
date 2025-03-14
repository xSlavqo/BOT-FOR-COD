# tasks/buffs.py

import time
import pyautogui
from control_game.screen_navigation import main_screen
from utils.helpers.locate import locate
from utils.general import read_config, write_config
from datetime import datetime, timedelta

class Buff:
    def __init__(self, name):
        self.name = name
        self.is_available = True

    @property
    def is_active(self):
        config = read_config()
        if self.name == "gather":
            return config.get(f"checkBox_buff_{self.name}", False)
        elif self.name in ["gold", "wood", "stone", "mana"]:
            return config.get("checkBox_buff_buff", False)
        return False

    @property
    def end_time(self):
        config = read_config()
        key = f"buff_{self.name}_end_time"
        end_time = config.get(key)
        return datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") if end_time else None

    @end_time.setter
    def end_time(self, value):
        key = f"buff_{self.name}_end_time"
        write_config(key, value.strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def is_running(self):
        return self.end_time and self.end_time > datetime.now()

    @staticmethod
    def enter_inv():
        if not main_screen():
            return False
        pyautogui.press("i")
        time.sleep(1)
        pyautogui.click(324, 621)
        return True

    def active_buff(self):
        if locate(f"png/buffs/{self.name}2_24.png", 0.99, 5, True):
            if locate("png/buffs/buff_start.png", 0.99, 5, True):
                self.end_time = datetime.now() + timedelta(hours=24)
                return True

        if locate(f"png/buffs/{self.name}2_8.png", 0.99, 5, True):
            if locate("png/buffs/buff_start.png", 0.99, 5, True):
                self.end_time = datetime.now() + timedelta(hours=8)
                return True

        self.is_available = False
        return True

    def __str__(self):
        return f"Buff(name={self.name}, is_active={self.is_active}, end_time={self.end_time})"

buffs = [Buff(name) for name in ["gather", "gold", "wood", "stone", "mana"]]

def monitor_buffs():
    active_not_running = [buff for buff in buffs if buff.is_active and not buff.is_running]

    if not active_not_running:
        return True

    active_not_running = [buff for buff in active_not_running if buff.is_available]

    if not active_not_running:
        return True

    if not Buff.enter_inv():
        return False

    for buff in active_not_running:
        buff.active_buff()

    return True
