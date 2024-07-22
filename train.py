import time
import re
from datetime import datetime, timedelta
from tools.locate import *
from tools.text import *
from tools.functions import save_data, open_data, load_config
from tasks.location import *



def train():
    config = load_config()
    times = open_data("train.txt")
    current_time = datetime.now()
    
    for key in ["vest", "arch", "inf", "cav"]:
        if not config.get(key):
            print(f"Brak zgody konfiguracji dla {key}.")
        else:
            if key in times:
                try:
                    train_time = datetime.strptime(times[key], '%Y-%m-%d %H:%M:%S.%f')
                    if train_time < current_time:
                        check_train(key)
                    else:
                        print(f"Czas dla {key} jeszcze nie minął: {times[key]}")
                except ValueError:
                    print(f"Nieprawidłowy format daty dla klucza {key}: {times[key]}")
            else:
                check_train(key)


def check_train(unit_type):
    city()
    time.sleep(1)
    if not locate_and_click(f"pngs/units/{unit_type}/place.png", 0.99, 0, 0, 10):
        return train(unit_type)
    time.sleep(1)
    if locate_and_click("pngs/units/speed.png", 0.99, 0, 0, 10):
        time.sleep(1)
        train_end(unit_type)
        return True
    return False
  
def train_end(unit_type):
    remaining_time = text((888, 314, 247, 25))
    match = re.search(r'(\d+):(\d+):(\d+)', remaining_time)
    if match:
        hours, minutes, seconds = [int(i) for i in match.groups()]
        time_to_add = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        end_time = datetime.now() + time_to_add
        save_data(unit_type, end_time, "train.txt")


 

# Przykład użycia
train()
