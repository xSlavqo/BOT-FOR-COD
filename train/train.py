# train/train.py

from train.train_utils import click_building_coordinates
from utils.locate import locate
from datetime import datetime, timedelta
import time
import time
from control_game.screen_navigation import *
from utils.text_recognition import capture_and_read_text
from train.train_utils import *

class Train:
    def __init__(self, name):
        self.name = name
        self.active = False
        self.train_end_time = None

def create_train_objects():
    comboBox_names = ["vest", "arch", "inf", "cav", "cele"]
    return [Train(name=name) for name in comboBox_names]

def check_train(trains, config_path):
    config = read_config(config_path)
    for train in trains:
        combo_key = f"comboBox_{train.name}"
        train.active = config.get(combo_key, 0) > 0

        if train.active:
            train.train_end_time = read_train_end_time(config, train.name)
            if train.train_end_time is None:
                check_train_end_time(train, config)

def check_train_end_time(train):
    map()
    if not city():
        return False

    click_building_coordinates(train.name)
    time.sleep(1)

    template_path = f"png/train/{train.name}.png"
    if not locate(template_path, 0.99, 5, True):
        return False

    if locate("png/train/queue_speed.png", 0.99):
        end_time_text = capture_and_read_text((1105, 718, 1390, 741))
        if end_time_text != "Not Found":
            print("jest")
            end_time = end_time_text
        else:
            end_time = "00:30:00"
            print("nie ma")
        hours, minutes, seconds = map(int, end_time.split(":"))
        added_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        current_time = datetime.now()
        calculated_time = current_time + added_time

        config = read_config()
        save_train_end_time(config, train.name, calculated_time)
    else:
        print("No queue found. Starting a new queue.")

