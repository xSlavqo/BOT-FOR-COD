# train/train.py

from train.train_utils import click_building_coordinates, save_train_end_time, read_config
from utils.locate import locate
from datetime import datetime, timedelta
import pyautogui
import time
from utils.text_recognition import capture_and_read_text


class TrainingBuilding:
    def __init__(self, name, tier=0):
        self.name = name
        self.tier = tier
        self.active = tier > 0
        self.train_end_time = None


def create_training_buildings(config_path="config.json"):
    building_names = ["vest", "arch", "inf", "cav", "cele"]
    config = read_config(config_path)
    buildings = []
    for name in building_names:
        tier = config.get(f"comboBox_{name}", 0)
        print(f"Building: {name}, Tier from config: {tier}")  # Debugowanie
        train_end_time = config.get(f"{name}_end_time")
        building = TrainingBuilding(name=name, tier=tier)
        if train_end_time:
            building.train_end_time = datetime.fromisoformat(train_end_time)
        buildings.append(building)
    return buildings



def calculate_end_time(end_time_text):
    try:
        hours, minutes, seconds = map(int, end_time_text.split(":"))
        return datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)
    except ValueError:
        return datetime.now() + timedelta(minutes=30)  # Domyślny czas 30 minut


def check_train_end_time(building):
    if not navigate_to_city():
        return False

    click_building_coordinates(building.name)
    click_building_coordinates(building.name)
    time.sleep(1)

    template_path = f"png/train/{building.name}.png"
    if not locate(template_path, 0.96, 5, True):
        return False

    if locate("png/train/queue_speed.png", 0.99):
        end_time_text = capture_and_read_text((1105, 718, 1390, 741))
        calculated_time = calculate_end_time(end_time_text if end_time_text != "Not Found" else "00:30:00")
        building.train_end_time = calculated_time
        save_train_end_time(read_config(), building.name, calculated_time)
        return True

    # Standardowe koordynaty dla większości budynków
    coordinates_standard = {
        'T1': (457, 871),
        'T2': (569, 873),
        'T3': (679, 871),
        'T4': (789, 871),
        'T5': (900, 870)
    }

    # Specjalne koordynaty dla obiektu "cele"
    coordinates_cele = {
        'T3': (568, 874),
        'T4': (680, 876),
        'T5': (791, 874)
    }

    # Mapowanie tier dla "cele" (0 = OFF, 1 = T3, 2 = T4, 3 = T5)
    if building.name == "cele":
        tier_mapping = {0: "OFF", 1: "T3", 2: "T4", 3: "T5"}
        tier_key = tier_mapping.get(building.tier, "OFF")
    else:
        tier_key = f"T{building.tier}"

    print(f"Building: {building.name}, Tier: {building.tier}, Tier Key: {tier_key}")

    # Wybierz odpowiednie koordynaty w zależności od obiektu
    coordinates = coordinates_cele if building.name == "cele" else coordinates_standard
    coords = coordinates.get(tier_key)

    if not coords:
        print(f"Nie ma koord dla {building.name} z tier {building.tier}")
        return False  # Jeśli tier jest nieobsługiwany, pomijamy

    pyautogui.click(coords)
    time.sleep(0.5)
    end_time_text = capture_and_read_text((1105, 718, 1390, 741))
    calculated_time = calculate_end_time(end_time_text if end_time_text != "Not Found" else "00:30:00")
    building.train_end_time = calculated_time
    save_train_end_time(read_config(), building.name, calculated_time)
    locate("png/train/train_start.png", 0.98, 5, True)
    return True


def navigate_to_city():
    try:
        from control_game.screen_navigation import map, city
        map()
        if not city():
            return False
    except Exception:
        return False
    return True
