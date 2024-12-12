# train/train.py

from datetime import datetime, timedelta
import pyautogui
import time
import re

from train.train_utils import save_train_end_time, read_config
from utils.locate import locate
from utils.text_recognition import capture_and_read_text


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
        train_end_time = config.get(f"{self.name}_end_time")
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
                except Exception:
                    pass

    def enter_building(self):
        if self._try_enter_building():
            return True
    
        try:
            from control_game.screen_navigation import map, city
            map()
            if not city():
                return False
        except Exception:
            return False
    
        return self._try_enter_building()
    
    def _try_enter_building(self):
        self._click_coordinates()
        template_path = f"png/train/{self.name}.png"
        return locate(template_path, 0.96, 5, True)


def calculate_end_time(end_time_text):
    try:
        clean_time = end_time_text.strip()
        hours, minutes, seconds = map(int, clean_time.split(":"))
        return datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)
    except ValueError as e:
        print(f"calculate_end_time błąd: '{end_time_text}', błąd: {e}")
        return datetime.now() + timedelta(minutes=30)

def check_train_end_time(self):
    if not self.enter_building():
        return False

    if locate("png/train/queue_speed.png", 0.99):
        end_time_text = capture_and_read_text((1105, 718, 1390, 741))
        calculated_time = self.calculate_end_time(end_time_text if end_time_text != "Not Found" else "00:30:00")
        self.train_end_time = calculated_time
        save_train_end_time(read_config(), self.name, calculated_time)
        return True

    return self.create_new_training_task()

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

    print(f"Building: {self.name}, Tier: {self.tier}, Tier Key: {tier_key}")

    coordinates = coordinates_cele if self.name == "cele" else coordinates_standard
    coords = coordinates.get(tier_key)

    if not coords:
        print(f"Nie ma koord dla {self.name} z tier {self.tier}")
        return False

    pyautogui.click(coords)
    time.sleep(0.5)
    end_time_text = capture_and_read_text((1105, 718, 1390, 741))
    if re.match(r'^\d{1,2}:\d{2}:\d{2}$', end_time_text):
        calculated_time = calculate_end_time(end_time_text)
    else:
        calculated_time = calculate_end_time("00:30:00")
    self.train_end_time = calculated_time
    save_train_end_time(read_config(), self.name, calculated_time)
    locate("png/train/train_start.png", 0.98, 5, True)
    return True


class TrainingManager:
    @staticmethod
    def create_training_buildings(config_path="config.json"):
        building_names = ["vest", "arch", "inf", "cav", "cele"]
        config = read_config(config_path)
        buildings = [TrainingBuilding(name=name) for name in building_names]
        for building in buildings:
            building.update_attributes(config)  
        return buildings

    @staticmethod
    def update_building_attributes(buildings):
        for building in buildings:
            building.update_attributes()

    @staticmethod
    def monitor_trainings():
        try:
            buildings = TrainingManager.create_training_buildings()
            for building in buildings:
                config = read_config()
                building.update_attributes(config)
                if building.active and building.train_end_time and building.train_end_time <= datetime.now():
                    if not building.check_train_end_time():
                        print(f"Błąd podczas aktualizacji budynku: {building.name}")
                    else:
                        print(f"Zaktualizowano czas dla budynku: {building.name}")
        except Exception as e:
            print(f"monitor_trainings - Critical Error: {e}")