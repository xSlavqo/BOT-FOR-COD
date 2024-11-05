# legions.py
import time
import pyautogui
import re
import pyautogui
from control_game.screen_navigation import *
from legions_status.legions_helper import locate_and_read_legions_status
from utils.locate import locate

def legions_menu():
    if not locate("png/legions/legions.png", 0.999):
        main_screen()
        pyautogui.press("j")
        if not locate("png/legions/legions.png", 0.999):
            return False
    return True

def legions():
    if legions_menu():
        if not locate("png/legions/legions.png", 0.99):
            return 1
        return locate_and_read_legions_status()
    return 1
