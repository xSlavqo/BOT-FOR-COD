# hospital.py
import pyautogui
import time
from utils.helpers.locate import locate
from control_game.screen_navigation import city

def check_hospital():
    if city():
        if locate("png/hospital.png", 0.94, 5, True):
            if locate("png/heal.png", 0.94, 5, True):
                time.sleep(0.5)
                pyautogui.press("esc")
                return True
            else:
                return False
        else:
            return True
    return False
