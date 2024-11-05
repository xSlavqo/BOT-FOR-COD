#rss.py

import time
import random
import pyautogui
from gui_utils import get_checkbox_state
from legions_status.legions import legions
from control_game.screen_navigation import *
from utils.locate import locate

def rss():
    for _ in range(legions()):
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
            time.sleep(0.2 )
        if not locate("png/rss_gather.png", 0.99, 5, True):
            continue
        if not locate("png/make_legion.png", 0.99, 5, True):
            return False
        locate("png/one_hero.png", 0.99, 5, True)
        if not locate("png/march.png", 0.99, 5, True):
            return False
        return True
    

def rss_type():
    selected_resources = []
    
    if get_checkbox_state("checkBox_goldmap"):
        selected_resources.append(1)
    if get_checkbox_state("checkBox_woodmap"):
        selected_resources.append(2)
    if get_checkbox_state("checkBox_stonemap"):
        selected_resources.append(3)
    if get_checkbox_state("checkBox_manamap"):
        selected_resources.append(4)
    
    if not selected_resources:
        print("Brak dostępnych zasobów do wyboru.")
        return False
    
    tried_resources = set()
    
    while len(tried_resources) < len(selected_resources):
        selected_option = random.choice([opt for opt in selected_resources if opt not in tried_resources])
        tried_resources.add(selected_option)
        
        if selected_option == 1:
            pyautogui.click(735, 1005)
        elif selected_option == 2:
            pyautogui.click(955, 1005)
        elif selected_option == 3:
            pyautogui.click(1175, 1005)
        elif selected_option == 4:
            pyautogui.click(1395, 1005)
        
        if locate("png/rss_find.png", 0.99, 5, True):
            time.sleep(1)
            if locate("png/rss_find.png", 0.99, 5, True):
                if len(selected_resources) == 1:
                    print("Nie udało się wybrać zasobu do zbierania, brak innych opcji.")
                    return False
                print("Odnaleziono ponownie opcję zbierania, losowanie innego zasobu.")
            else:
                return True
        else:
            return True
    
    print("Nie udało się wybrać zasobu do zbierania.")
    return False
