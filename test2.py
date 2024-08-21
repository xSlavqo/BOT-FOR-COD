from datetime import datetime, timedelta
import re
from tools.functions import save_data, open_data, load_config
from tasks.location import *
from tools.locate import *
from tools.text import *



def check_autobuild():
    coordinates = load_building_coordinates()
    city()
    time.sleep(1)  
    buildings = coordinates.get("buildings")
    pyautogui.mouseDown(buildings)
    pyautogui.mouseUp(buildings)
    if locate_and_click("pngs/build2.png", 0.97, 2):
        if locate_and_click("pngs/build3.png", 0.97, 2):
            auto_build()
        else:
            check_for_slot1()
            time.sleep(2)
            coordinates = load_building_coordinates()
            buildings = coordinates.get("buildings")
            pyautogui.mouseDown(buildings)
            pyautogui.mouseUp(buildings)
            pyautogui.mouseDown(buildings)
            pyautogui.mouseUp(buildings)
            time.sleep(1)
            if locate_and_click("pngs/build2.png", 0.97, 2):
                time.sleep(2)
                check_for_slot2()


def auto_build():
    locate_and_click("pngs/build4.png", 0.97, 2)
    locate_and_click("pngs/build5.png", 0.97, 2)
    time.sleep(1)
    pyautogui.click(960, 463)

def check_for_slot1():
    time_build1 = text((1358, 591, 120, 32), invert_colors=1, tolerance=240, blur_ksize=1)
    pyautogui.click(1415, 592)
    time.sleep(1)
    build1 = text((1157, 320, 46, 25), invert_colors=1, tolerance=240, blur_ksize=1)
    if '/' in build1:
        licznik, mianownik = build1.split('/')
        licznik = int(licznik)
        mianownik = int(mianownik)
        
        if licznik == mianownik:
            time_build1 = re.search(r'(\d+):(\d+):(\d+)', time_build1)
            if time_build1:
                hours, minutes, seconds = [int(i) for i in time_build1.groups()]
                time_to_add = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                end_time = datetime.now() + time_to_add
                save_data("build1", end_time, "times.txt")
    pyautogui.press("esc")

def check_for_slot2():
    time_build2 = text((1353, 780, 139, 31), invert_colors=1, tolerance=240, blur_ksize=1)
    print(time_build2)
    pyautogui.click((1415, 778))
    time.sleep(1)
    build2 = text((1157, 320, 46, 25), invert_colors=1, tolerance=240, blur_ksize=1)
    if '/' in build2:
        licznik, mianownik = build2.split('/')
        licznik = int(licznik)
        mianownik = int(mianownik)
        
        if licznik == mianownik:
            time_build2 = re.search(r'(\d+):(\d+):(\d+)', time_build2)
            if time_build2:
                hours, minutes, seconds = [int(i) for i in time_build2.groups()]
                time_to_add = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                end_time = datetime.now() + time_to_add
                save_data("build2", end_time, "times.txt")
    pyautogui.press("esc")

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

check_autobuild()