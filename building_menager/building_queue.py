# building_manager/build_queue.py

import re
import pyautogui
import time
from datetime import datetime, timedelta
from tools.locate import *
from tools.text import text
from building_menager.building_operations import BuildingOperations

class BuildQueue:
    __slots__ = ['id', 'unlocked', 'time_end', 'region', 'sett_button', 'operations']

    def __init__(self, id):
        self.id = id
        self.unlocked = None
        self.time_end = None
        self.operations = BuildingOperations()

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

    def check_if_unlocked(self, building):
        if not self.operations.open_building(building, 1):
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
        return False

    def set_time_end(self, time_end):
        self.time_end = time_end

    def time_update(self):
        helps = text((1157, 320, 46, 25), invert_colors=1, tolerance=240, blur_ksize=1)
        if '/' in helps:
            licznik, mianownik = map(int, helps.split('/'))
            if licznik == mianownik:
                remaining_time = text((946, 311, 175, 33), invert_colors=1, tolerance=240, blur_ksize=1)
                match = re.search(r'(\d+):(\d+):(\d+)', remaining_time)
                if match:
                    hours, minutes, seconds = map(int, match.groups())
                    self.set_time_end(datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds))

            else:
                self.set_time_end(datetime.now() + timedelta(minutes=10))
        pyautogui.press("esc")

    def start_upgrade(self):
        time.sleep(1)
        self.set_time_end(datetime.now() + timedelta(seconds=10))
        locate_and_click("pngs/queue_upgrade_start.png", 0.97, 2)
        time.sleep(1)
        locate_and_click("pngs/ask_help.png", 0.95, 3)

    def control_queue(self, building):
        if self.unlocked is None:
            self.check_if_unlocked(building)
        if not self.unlocked:
            print(f"Kolejka {self.id} jest zablokowana.")
            return
        if self.check_time():
            time_remaining = self.time_end - datetime.now()
            hours, minutes = divmod(time_remaining.total_seconds() // 60, 60)
            seconds = time_remaining.total_seconds() % 60
            print(f"Kolejka {self.id} jest zajęta. Pozostały czas: {int(hours)} godziny, {int(minutes)} minuty, {int(seconds)} sekundy.")
        else:
            if not self.operations.open_building(building, 1):
                print("Błąd wejścia do budynku kolejek budowania.")
                return
            time.sleep(0.5)
            if locate_and_click_in_region("pngs/queue_run.png", 0.96, region=self.region):
                if locate_and_click("pngs/building_upgrade.png", 0.99, 2):
                    print("Rozpoczynam ulepszanie ...")
                    self.start_upgrade()
                elif locate("pngs/build_new.png", 0.99):
                    print("Buduje nowy budynek ...")
                    time.sleep(1)
                    pyautogui.click(298, 746)
                    locate_and_click("pngs/build_new_start.png", 0.97, 2)
                    time.sleep(20)
                    print("Restart funkcji po 20 sekundach...")
                    self.control_queue(building)
            elif locate_and_click_in_region("pngs/queue_speedup.png", 0.96, region=self.region):
                print(f"Kolejka {self.id} jest zajęta, aktualizuje czas zakończenia ...")
                time.sleep(1)
                self.time_update()
            else:
                time.sleep(0.5)
                self.check_if_unlocked(building)
