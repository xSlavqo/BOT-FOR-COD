from tools.locate import *
from tasks.location import main_screen
import pyautogui
import time

def ally_help():
    main_screen()
    locate_and_click("pngs/ally_help.png", 0.99) 

def ally_menu():
    if not locate("pngs/ally_menu.png", 0.99):
        main_screen()
        pyautogui.press("o")
        time.sleep(1) 
        return ally_menu()
    return True

def ally_gifts():
    ally_menu()
    locate_and_click("pngs/ally_gifts.png", 0.99)
    time.sleep(1)
    pyautogui.click(1142, 432)
    time.sleep(0.5)
    while locate_and_click("pngs/ally_gifts_collect.png", 0.98):
        time.sleep(0.5)
    pyautogui.click(924, 432)
    time.sleep(0.5)
    while locate_and_click("pngs/ally_gifts_collect.png", 0.98):
        time.sleep(0.5)
    pyautogui.press("esc")

