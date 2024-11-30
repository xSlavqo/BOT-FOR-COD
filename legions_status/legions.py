# legions.py
import time
import pyautogui
from control_game.screen_navigation import main_screen
from legions_status.legions_helper import locate_and_read_legions_status
from utils.locate import locate

def legions_menu():
    if locate("png/legions/legions_menu.png", 0.99):
        return True
    main_screen()
    pyautogui.press("j")
    return locate("png/legions/legions_menu.png", 0.99)

def legions():
    if not legions_menu():
        return 1
    if not locate("png/legions/legions.png", 0.99):
        return 1
    return locate_and_read_legions_status()
