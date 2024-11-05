#screen_navigation.py

import pyautogui
import time
from utils.locate import locate

def check_and_navigate(target_image, alt_image, esc_attempts=0, space_attempts=0):
    max_esc_presses = 10
    max_space_presses = 3

    if locate(target_image, 0.99, 3):
        return True
    elif locate(alt_image, 0.99, 3):
        if space_attempts < max_space_presses:
            pyautogui.press('space')
            time.sleep(1)
            return check_and_navigate(target_image, alt_image, esc_attempts, space_attempts + 1)
        else:
            print("Nie można odnaleźć odpowiedniego widoku")
            return False
    else:
        if esc_attempts < max_esc_presses:
            pyautogui.press('esc')
            time.sleep(1)
            return check_and_navigate(target_image, alt_image, esc_attempts + 1, space_attempts)
        else:
            print("Nie można odnaleźć main_screenn")
            return False

def city():
    return check_and_navigate("png/city.png", "png/map.png")

def map():
    return check_and_navigate("png/map.png", "png/city.png")

def main_screen():
    escape_attempts = 0
    max_esc_presses = 10
    while not (locate("png/map.png", 0.99, 3) or locate("png/city.png", 0.99, 3)):
        if escape_attempts >= max_esc_presses:
            print("Nie można odnaleźć main_screen")
            return False
        pyautogui.press("esc")
        escape_attempts += 1
        time.sleep(1)
    return True

def ally_menu():
    if locate("png/ally_menu.png", 0.99, 3):
        return True
    else:
        main_screen()
        time.sleep(1)
        pyautogui.press("o")
        if locate("png/ally_menu.png", 0.99, 3):
            return True
        else:
            print("Nie udało się odnaleźć ally_menu")
            return False
