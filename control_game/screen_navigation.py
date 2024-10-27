#screen_navigation.py

import pyautogui
import time
from utils.locate import locate

def check_and_navigate(target_image, alt_image):
    if locate(target_image, 0.99, 3):
        return True
    elif locate(alt_image, 0.99, 3):
        pyautogui.press('space')
        time.sleep(1)
        return check_and_navigate(target_image, alt_image)
    else:
        pyautogui.press('esc')
        time.sleep(1)
        return check_and_navigate(target_image, alt_image)

def city():
    return check_and_navigate("png/city.png", "png/map.png")

def map():
    return check_and_navigate("png/map.png", "png/city.png")

def main_screen():
    while not (locate("png/map.png", 0.99, 3) or locate("png/city.png", 0.99, 3)):
        pyautogui.press("esc")
        time.sleep(1)
    return True

def ally_menu():
    if not locate("png/ally_menu.png", 0.99, 3):
        main_screen()
        pyautogui.press("o")
        time.sleep(1)
        return ally_menu()
    return True

