import pyautogui
import time
import re
from tools.locate import locate, locate_and_click
from tasks.location import city, map
from tools.text import text

def open_building(building, action=None):
    map_checked = False
    
    while True:
        city()
        pyautogui.mouseDown(x=building.position_x, y=building.position_y)
        pyautogui.mouseUp(x=building.position_x, y=building.position_y)
        
        if locate(f'pngs/building/{building.name}.png', 0.98):
            print("Znaleziono budynek!")
            if action == 1:
                locate_and_click(f'pngs/building/{building.name}.png', 0.98)
            elif action == 2:
                locate_and_click("pngs/info.png", 0.98)
            return True
        elif locate("pngs/building_work.png", 0.98):
            print("Budynek jest w trakcie pracy!")
            return False
        elif locate("pngs/info.png", 0.98):
            print("Przeszkoda na budynku!")
            return False
        elif not map_checked:
            print("Złe koordynaty budynku! Powtarzam szukanie!")
            map()
            map_checked = True
        else:
            print("Złe koordynaty budynku! Kończę szukanie!")
            return False

def check_lvl(building):
    if open_building(building, 2):
        time.sleep(1)
        info = text((987, 529, 427, 66), invert_colors=0, tolerance=240, blur_ksize=1)
        match = re.search(r'Poziom\s(\d+)', info)
        if match:
            building.level = int(match.group(1))
            return building.level
        else:
            print("Nie znaleziono poziomu budynku.")
            return None
    else:
        print("Nie udało się otworzyć budynku.")
        return None
