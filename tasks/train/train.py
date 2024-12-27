# tasks/train/train.py

from datetime import datetime, timedelta
import pyautogui
import time
import re

from tasks.train.train_utils import save_train_end_time, read_config
from utils.helpers.locate import locate
from utils.helpers.text_recognition import text_recognition


class TrainingBuilding:
    def __init__(self, name, tier=0):
        self.name = name
        self.tier = tier
        self.active = tier > 0
        self.coordinates = None
        self.train_end_time = None
        self.update_attributes()

    def update_attributes(self, config=None):
        if config is None:
            config = read_config()
        
        self.tier = config.get(f"comboBox_{self.name}", 0)
        self.active = self.tier > 0
        self.coordinates = config.get(self.name)
        train_end_time = config.get(f"{self.name}_train_end_time")
        self.train_end_time = datetime.fromisoformat(train_end_time) if train_end_time else None

    def _click_coordinates(self):
        if self.coordinates:
            x, y = self.coordinates.get("X"), self.coordinates.get("Y")
            if x is not None and y is not None:
                try:
                    pyautogui.moveTo(x, y)
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                    pyautogui.moveTo(x, y)
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                    time.sleep(1)
                except Exception as e:
                    raise Exception(f"Błąd w _click_coordinates: {e}")

    def enter_building(self):
        if self._try_enter_building():
            return True
    
        try:
            from control_game.screen_navigation import map, city
            map()
            if not city():
                return False
        except Exception as e:
            raise Exception(f"Błąd w enter_building: {e}")
        return self._try_enter_building()
    
    def _try_enter_building(self):
        self._click_coordinates()
        template_path = f"png/train/{self.name}.png"
        return locate(template_path, 0.96, 5, True)

    def check_train_end_time(self):
        if not self.enter_building():
            raise Exception("Nie udało się wejść do budynku")
        
        if locate("png/train/queue_speed.png", 0.99, 2):
            return self.update_training_task()
        else:
            return self.create_new_training_task()
    
    def update_training_task(self):
        end_time_text = text_recognition((1149, 705, 218, 48)) or "00:30:00"
        calculated_time = calculate_end_time(end_time_text)
        self.train_end_time = calculated_time
        save_train_end_time(read_config(), self.name, calculated_time)
        pyautogui.press("esc")
        time.sleep(1)
        return True



    def create_new_training_task(self):
        coordinates_standard = {
            'T1': (457, 871),
            'T2': (569, 873),
            'T3': (679, 871),
            'T4': (789, 871),
            'T5': (900, 870)
        }

        coordinates_cele = {
            'T3': (568, 874),
            'T4': (680, 876),
            'T5': (791, 874)
        }

        if self.name == "cele":
            tier_mapping = {0: "OFF", 1: "T3", 2: "T4", 3: "T5"}
            tier_key = tier_mapping.get(self.tier, "OFF")
        else:
            tier_key = f"T{self.tier}"

        coordinates = coordinates_cele if self.name == "cele" else coordinates_standard
        coords = coordinates.get(tier_key)

        if not coords:
            raise Exception(f"Nie ma koordynatów dla {self.name} z tier {self.tier}")

        pyautogui.click(coords)
        time.sleep(1)
        end_time_text = text_recognition((1274, 875, 233, 42)) or "00:30:00"
        calculated_time = calculate_end_time(end_time_text)
        self.train_end_time = calculated_time
        save_train_end_time(read_config(), self.name, calculated_time)
        if locate("png/train/train_start.png", 0.98, 5, True):
            return True
        return False



def calculate_end_time(end_time_text):
    clean_time = end_time_text.strip()
    hours, minutes, seconds = map(int, clean_time.split(":"))
    return datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)


buildings = [TrainingBuilding(name) for name in ["vest", "arch", "inf", "cav", "cele"]]

def monitor_trainings():
    for building in buildings:
        building.update_attributes()
        if not building.active:
            continue
        if building.train_end_time is None or building.train_end_time <= datetime.now():
            if not building.check_train_end_time():
                raise Exception(f"Błąd podczas aktualizacji budynku: {building.name}")
    
    return True
