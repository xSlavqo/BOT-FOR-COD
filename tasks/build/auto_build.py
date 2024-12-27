# auto_build.py
import pyautogui
import time
from control_game.screen_navigation import *
from tasks.build.build_helper import text_locator
from utils.locate import locate

def auto_build():
    if not city():
        return False
    time.sleep(1)
    if not text_locator("png/build/build1.png", "buduj"):
        return True
    if not locate("png/build/build2.png", 0.95, 5, True):
        return False
    if not locate("png/build/build3.png", 0.98, 5, True):
        return False
    if not locate ("png/build/build4.png", 0.99, 5, True):
        pyautogui.mouseDown(292, 792); pyautogui.mouseUp(292, 792)
        if not locate("png/build/build_new.png", 0.99, 5, True):
            return False
    else:
        if not locate("png/build/build5.png", 0.95, 5, True):
            return False
        
    click_count = 0
    while click_count < 3 and locate("png/build/help_ask.png", 0.95, 2, True):
        click_count += 1
        time.sleep(0.5)

    return True