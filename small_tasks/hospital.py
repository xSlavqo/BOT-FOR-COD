# hospital.py
import pyautogui
from utils.locate import locate
from control_game.screen_navigation import city

def check_hospital():
    if city():
        if locate("png/hospital.png", 0.94, 5, True):
            locate("png/heal.png", 0.94, 5, True)
            pyautogui.press("esc")
            return True
    return False
