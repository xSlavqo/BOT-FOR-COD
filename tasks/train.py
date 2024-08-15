import time
import re
from datetime import datetime, timedelta
from tools.locate import *
from tools.text import *
from tools.functions import save_data, open_data, load_config
from tools.find import *
from tasks.location import *



def train_units():
    config = load_config()
    times = open_data("train.txt")
    current_time = datetime.now()
    
    for unit_type in ["vest", "arch", "inf", "cav"]:
        if not config.get(unit_type):
            print(f"Brak zgody konfiguracji dla {unit_type}.")
        else:
            if unit_type in times:
                try:
                    train_time = datetime.strptime(times[unit_type], '%Y-%m-%d %H:%M:%S.%f')
                    if train_time < current_time:
                        train_unit(unit_type)
                    else:
                        print(f"Czas dla {unit_type} jeszcze nie minął: {times[unit_type]}")
                except ValueError:
                    print(f"Nieprawidłowy format daty dla klucza {unit_type}: {times[unit_type]}")
            else:
                train_unit(unit_type)

 
def train_unit(unit_type):
    city()
    time.sleep(1)
    find_and_click(f"pngs/units/{unit_type}", 0.3)
    time.sleep(1)
    if locate_and_click("pngs/units/speed.png", 0.99):
        time.sleep(1)
        train_end_time(unit_type)
        return
    start_train(unit_type)
  
def train_end_time(unit_type):
    remaining_time = text((888, 314, 247, 25))
    match = re.search(r'(\d+):(\d+):(\d+)', remaining_time)
    if match:
        hours, minutes, seconds = [int(i) for i in match.groups()]
        time_to_add = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        end_time = datetime.now() + time_to_add
        save_data(unit_type, end_time, "train.txt")

coordinates = {
    'T1': (457, 871),
    'T2': (569, 873),
    'T3': (679, 871),
    'T4': (789, 871),
    'T5': (900, 870)
}

def start_train(unit_type):
    config = load_config()
    if find_and_click("pngs/units/train", 0.5):
        time.sleep(1)
        value = config.get(unit_type + "_tier")
        if value:
            pyautogui.click(coordinates.get(value))
            time.sleep(1)
            locate_and_click("pngs/train_start.png", 0.99)