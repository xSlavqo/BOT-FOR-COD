import pyautogui
import time
from tools.locate import *

def city():
    if locate("pngs/city", 0.99):
        return True
    elif locate("pngs/map", 0.99):
        pyautogui.press('space')
        time.sleep(1)
        return city()
    else:
        pyautogui.press('esc')
        time.sleep(1)
        return city()

def map():
    if locate("pngs/map", 0.99):
        return True
    elif locate("pngs/city", 0.99):
        pyautogui.press('space')
        time.sleep(1)
        return map()
    else:
        pyautogui.press('esc')
        time.sleep(1)
        return map()
    
def main_screen():
    while not (locate("pngs/map", 0.99) or locate("pngs/city", 0.99)):
        pyautogui.press("esc")
        time.sleep(1)
    return True