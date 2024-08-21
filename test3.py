import re
import pyautogui
import time
from datetime import datetime, timedelta
from tools.functions import save_data, open_data, load_config
from tasks.location import *
from tools.locate import *
from tools.text import *


class BuildQueue:
    __slots__ = ['id', 'is_unlocked', 'time_end', 'coordinates']

    def __init__(self, id, coordinates, is_unlocked=False):
        self.id = id
        self.coordinates = coordinates
        self.is_unlocked = is_unlocked
        self.time_end = None

    def check_if_unlocked(self):
        self.is_unlocked = not locate_in_region("2.png", 0.95, self.coordinates)
        return self.is_unlocked
    
    def check_if_busy(self):
        if self.time_end:
            if datetime.now() < self.time_end:
                return True
            else:
                self.time_end = None
        time.sleep(1)
        if locate_in_region("pngs/build3.png", 0.99, self.coordinates):
            return False
        return True
    
    def set_time_end(self, time_end):
        self.time_end = time_end
                

def enter_building():
    if locate("1.png", 0.95) is True:
        return True
    else:
        map()
        coordinates = load_building_coordinates()
        city()
        time.sleep(1)
        buildings = coordinates.get("buildings")
        pyautogui.mouseDown(buildings)
        pyautogui.mouseUp(buildings)
        if locate_and_click("pngs/build2.png", 0.97, 2):
            return True
    
def load_building_coordinates():
    coordinates = {}
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "buildings.txt")
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                unit = lines[i].split('_')[0]
                x = int(lines[i].split('=')[1].strip())
                y = int(lines[i+1].split('=')[1].strip())
                coordinates[unit] = (x, y)
    except FileNotFoundError:
        print("Plik buildings.txt nie został znaleziony.")
    
    return coordinates


def start_build(queue):
    locate_and_click("pngs/build3.png", 0.97, 2)
    locate_and_click("pngs/build4.png", 0.97, 2)
    time.sleep(1)
    time_build = text((1324, 912, 123, 35), invert_colors=1, tolerance=240, blur_ksize=1)
    time_build = re.search(r'(\d+):(\d+):(\d+)', time_build)
    hours, minutes, seconds = [int(i) for i in time_build.groups()]
    time_to_add = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    end_time = datetime.now() + time_to_add
    queue.set_time_end(end_time)
    print(queue.time_end)
    locate_and_click("pngs/build5.png", 0.97, 2)
    locate_and_click("pngs/ask_help.png", 0.95, 3)

def check_and_control_queue(queue):
    if queue.time_end:    
        if queue.time_end > datetime.now():
            print(f"Queue {queue.id} is busy.")
    enter_building()
    time.sleep(1)
    if queue.check_if_unlocked():
        if queue.check_if_busy() == False:
            print(f"Queue {queue.id} is not busy. Starting start_build.")
            time.sleep(3)
            start_build(queue)
            
        else:
            print(f"Queue {queue.id} is busy.")
    else:
        print(f"Queue {queue.id} is locked.")

def auto_build():
    queue1 = None
    queue2 = None
    if not queue1:
            queue1 = BuildQueue(1, (380, 485, 1177, 191))
    if not queue2:
        queue2 = BuildQueue(2, (383, 690, 1175, 172))
    check_and_control_queue(queue1)
    check_and_control_queue(queue2)
