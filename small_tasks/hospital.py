# hospital.py
import pyautogui
import time
from utils.locate import locate
from control_game.screen_navigation import city

def check_hospital():
    if city():
        if locate("png/hospital.png", 0.94, 5, True):
            if locate("png/heal.png", 0.94, 5, True):
                time.sleep(0.5)
                pyautogui.press("esc")
                return True
            else:
                print("Nie udało się odnaleźć przycisku leczenia!")
                return False
        else:
            print("Brak jednostek do leczenia.")
            return True
    return False
