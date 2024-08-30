import re
import pyautogui
import time
from datetime import datetime, timedelta
from tasks.location import *
from tools.locate import *
from tools.text import *

class BuildQueue:
    __slots__ = ['id', 'unlocked', 'time_end', 'region', 'sett_button']

    def __init__(self, id):
        self.id = id
        self.unlocked = None
        self.time_end = None

        if id == 1:
            self.region = (380, 485, 1177, 191)
            self.sett_button = (1412, 590)
            self.unlocked = True
        elif id == 2:
            self.region = (386, 690, 1153, 194)
            self.sett_button = (1411, 782)
        else:
            self.region = (0, 0, 0, 0) 
            self.sett_button = (0, 0) 

    def check_if_unlocked(self):
        if not enter_building():
            print("Failed to enter the building.")
            self.unlocked = None
            return self.unlocked
        if locate_in_region("pngs/queue_run.png", 0.95, region=self.region):
            self.unlocked = True
        elif locate_in_region("pngs/queue_lock.png", 0.95, region=self.region):
            self.unlocked = False
        return self.unlocked


    def check_time(self):
        if self.time_end and datetime.now() < self.time_end:
            return True
        self.time_end = None

    def set_time_end(self, time_end):
        self.time_end = time_end

    def time_update(self, time_end):
        helps = text((1157, 320, 46, 25), invert_colors=1, tolerance=240, blur_ksize=1)
        if '/' in helps:
            licznik, mianownik = helps.split('/')
            licznik = int(licznik)
            mianownik = int(mianownik)
            
            if licznik == mianownik:
                remaining_time = text((946, 311, 175, 33), invert_colors=1, tolerance=240, blur_ksize=1)
                remaining_time = re.search(r'(\d+):(\d+):(\d+)', remaining_time)
                if remaining_time:
                    hours, minutes, seconds = [int(i) for i in remaining_time.groups()]
                    time_to_add = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                    time_end = datetime.now() + time_to_add
            else:
                time_end = datetime.now() + timedelta(minutes=10)
        pyautogui.press("esc")
        self.time_end = time_end


def load_building_coordinates():
    region = {}
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "buildings.txt")
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                unit = lines[i].split('_')[0]
                x = int(lines[i].split('=')[1].strip())
                y = int(lines[i+1].split('=')[1].strip())
                region[unit] = (x, y)
    except FileNotFoundError:
        print("Plik buildings.txt nie został znaleziony.")
    return region

def enter_building():
    if locate("pngs/queue_home.png", 0.95):
        return True
    map()
    city()
    time.sleep(1)
    region = load_building_coordinates()
    buildings = region.get("buildings")
    pyautogui.mouseDown(buildings)
    pyautogui.mouseUp(buildings)
    time.sleep(0.5)
    if locate_and_click("pngs/queue_home_enter.png", 0.97, 2):
        return True

def start_upgrade(queue):
    time.sleep(1)
    queue.set_time_end(datetime.now() + timedelta(seconds=10))
    locate_and_click("pngs/queue_upgrade_start.png", 0.97, 2)
    time.sleep(1)
    if locate_and_click("pngs/ask_help.png", 0.95, 3):
        pass

def check_and_control_queue(queue):
    if queue.unlocked is None:
        enter_building() 
        queue.check_if_unlocked() 
    if queue.unlocked is False:
        print(f"Kolejka {queue.id} jest zablokowana.")
        return
    if queue.check_time():
        time_remaining = queue.time_end - datetime.now()
        minutes, seconds = divmod(time_remaining.total_seconds(), 60)
        hours, minutes = divmod(minutes, 60)
        print(f"Kolejka {queue.id} jest zajęta. Pozostały czas: {int(hours)} godziny, {int(minutes)} minuty, {int(seconds)} sekundy.")
    else:
        if not enter_building():
            print("Błąd wejścia do budynku kolejek budowania.")
            return 
        time.sleep(0.5)
        if locate_and_click_in_region("pngs/queue_run.png", 0.96, region=queue.region):
            if locate_and_click("pngs/building_upgrade.png", 0.99, 2):
                print("Rozpoczynam ulepszanie ...")
                start_upgrade(queue)
                return
            elif locate("pngs/build_new.png", 0.99):
                print("Buduje nowy budynek ...")
                time.sleep(1)
                pyautogui.click(298, 746)
                locate_and_click("pngs/build_new_start.png", 0.97, 2)
                time.sleep(20)
                print("Restart funkcji po 20 sekundach...")
                return check_and_control_queue(queue)
        elif locate_and_click_in_region("pngs/queue_speedup.png", 0.96, region=queue.region):
            print(f"Kolejka {queue.id} jest zajęta, aktualizuje czas zakończenia ...")
            time.sleep(1)
            queue.time_update(queue.time_end)
            return
        else:
            time.sleep(0.5)
            queue.check_if_unlocked() 
            return



def auto_build(variable_manager, variable_queue):
    if 'queue1' not in variable_manager.variables:
        queue1 = BuildQueue(1)
    else:
        queue1 = variable_manager.variables['queue1']

    if 'queue2' not in variable_manager.variables:
        queue2 = BuildQueue(2)
    else:
        queue2 = variable_manager.variables['queue2']

    check_and_control_queue(queue1)
    variable_queue.put(('queue1', queue1))
    check_and_control_queue(queue2)
    variable_queue.put(('queue2', queue2))
