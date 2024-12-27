# tasks/train/train_utils.py

import json
from datetime import datetime
import pyautogui

CONFIG_PATH = "config.json"

def read_config(file_path=CONFIG_PATH):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def read_train_end_time(config, train_name):
    end_time_key = f"{train_name}_train_end_time"
    if end_time_key in config:
        try:
            return datetime.strptime(config[end_time_key], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
    return None

def save_train_end_time(config, train_name, end_time, file_path=CONFIG_PATH):
    end_time_key = f"{train_name}_train_end_time"
    config[end_time_key] = end_time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(file_path, 'w') as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

def click_building_coordinates(building_name, config_path=CONFIG_PATH):
    config = read_config(config_path)
    if building_name in config:
        coords = config[building_name]
        x = coords.get("X")
        y = coords.get("Y")
        if x is not None and y is not None:
            try:
                pyautogui.moveTo(x, y)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
            except Exception:
                pass
