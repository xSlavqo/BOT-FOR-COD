# legions_status.rss.py

import time
import random
import pyautogui
from gui_utils import get_checkbox_state
from tasks.legions.legions import legions
from control_game.screen_navigation import *
from utils.helpers.locate import locate

def rss():
    legion_count = legions()
    if legion_count == 0:
        return True
    
    for _ in range(legion_count):
        if not map():
            return False
        time.sleep(1)
        pyautogui.press("f")
        time.sleep(1)
        
        if not rss_type():
            return False
        
        for _ in range(2):
            pyautogui.mouseDown(960, 540)
            pyautogui.mouseUp(960, 540)
            time.sleep(0.2)
        
        if not locate("png/rss_gather.png", 0.99, 5, True):
            continue
        if not locate("png/make_legion.png", 0.99, 5, True):
            return False
        
        locate("png/one_hero.png", 0.99, 5, True)
        
        if not locate("png/march.png", 0.99, 5, True):
            return False
        
    return True

    
def rss_type():
    resource_positions = {
        1: (735, 1005),
        2: (955, 1005),
        3: (1175, 1005),
        4: (1395, 1005)
    }

    selected_resources = [
        key for key, checkbox in zip(resource_positions.keys(), [
            "checkBox_goldmap", "checkBox_woodmap", "checkBox_stonemap", "checkBox_manamap"
        ]) if get_checkbox_state(checkbox)
    ]

    remaining_resources = [key for key in resource_positions.keys() if key not in selected_resources]

    if not selected_resources:
        print("Brak dostępnych zasobów do wyboru.")
        return False

    tried_resources = set()

    def try_locate_resource(option):
        if option in tried_resources:
            return False

        tried_resources.add(option)
        pyautogui.click(*resource_positions[option])

        if locate("png/rss_find.png", 0.99, 5, True):
            time.sleep(1)
            return not locate("png/rss_find.png", 0.99, 5, True)
        return True

    for resource in selected_resources:
        if try_locate_resource(resource):
            return True

    for resource in remaining_resources:
        if try_locate_resource(resource):
            return True

    print("Nie udało się wybrać zasobu do zbierania.")
    return False
