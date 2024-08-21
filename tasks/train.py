import time
import re
import pyautogui
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
    
    for unit_type in ["vest", "arch", "inf", "cav", "cele"]:
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
    coordinates = load_building_coordinates()
    if unit_type not in coordinates:
        print(f"Brak zapisanych współrzędnych dla {unit_type}.")
        return
    
    city()
    time.sleep(1)
    
    # Kliknięcie na odpowiednie współrzędne budynku za pomocą mouseDown i mouseUp
    x, y = coordinates[unit_type]
    pyautogui.mouseDown(x, y)
    time.sleep(0.1)
    pyautogui.mouseUp(x, y)
    time.sleep(1)
    
    if locate_and_click("pngs/units/speed.png", 0.98):
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
        save_data(unit_type, end_time, "times.txt")

coordinates = {
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

def start_train(unit_type):
    config = load_config()
    if locate_and_click("pngs/units/train", 0.97):
        time.sleep(1)
        value = config.get(unit_type + "_tier")
        if value:
            if unit_type == "cele":
                pyautogui.click(coordinates_cele.get(value))
            else:
                pyautogui.click(coordinates.get(value))
            time.sleep(1)
            remaining_time = text((1267, 828, 249, 97), invert_colors=1, tolerance=254, blur_ksize=3)
            match = re.search(r'(\d+):(\d+):(\d+)', remaining_time)
            if match:
                hours, minutes, seconds = [int(i) for i in match.groups()]
                time_to_add = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                end_time = datetime.now() + time_to_add
                save_data(unit_type, end_time, "times.txt")
                locate_and_click("pngs/train_start.png", 0.99)



def load_building_coordinates():
    coordinates = {}
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "buildings.txt")
    
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            unit = lines[i].split('_')[0]
            x = int(lines[i].split('=')[1].strip())
            y = int(lines[i+1].split('=')[1].strip())
            coordinates[unit] = (x, y)
    
    return coordinates