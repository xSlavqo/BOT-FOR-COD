#rss.py

import time
import random
import pyautogui
from gui_utils import get_checkbox_state
from legions_status.legions import legions
from control_game.screen_navigation import *
from utils.locate import locate

def rss():
    for _ in range(legions()):
        map()
        time.sleep(1)
        pyautogui.press("f")
        time.sleep(1)
        rss_type()
        locate("png/rss_find.png", 0.99, 5, True)
        if locate("png/rss_find.png", 0.99):
            pyautogui.press("esc")
            continue
        pyautogui.mouseDown(960, 540)
        pyautogui.mouseUp(960, 540) 
        time.sleep(0.2)
        pyautogui.mouseDown(960, 540)
        pyautogui.mouseUp(960, 540)
        time.sleep(1)
        if not locate("png/rss_gather.png", 0.99, 5, True):
            continue
        if not locate("png/make_legion.png", 0.99, 5, True):
            pyautogui.press("esc")
            continue
        locate("png/one_hero.png", 0.99, 5, True)
        locate("png/march.png", 0.99, 5, True)
    
def rss_type():
    print("type")
    selected_resources = []
    
    # Sprawdzamy stany checkboxów i dodajemy odpowiednie wartości do listy
    if get_checkbox_state("checkBox_goldmap"):
        selected_resources.append(1)
    if get_checkbox_state("checkBox_woodmap"):
        selected_resources.append(2)
    if get_checkbox_state("checkBox_stonemap"):
        selected_resources.append(3)
    if get_checkbox_state("checkBox_manamap"):
        selected_resources.append(4)
    
    # Jeśli żaden checkbox nie jest zaznaczony, wybieramy wszystkie
    if not selected_resources:
        selected_resources = [1, 2, 3, 4]
    
    # Losowy wybór i wykonanie kliknięcia na podstawie wybranego zasobu
    selected_option = random.choice(selected_resources)
    if selected_option == 1:
        pyautogui.click(735, 1005)
    elif selected_option == 2:
        pyautogui.click(955, 1005)
    elif selected_option == 3:
        pyautogui.click(1175, 1005)
    elif selected_option == 4:
        pyautogui.click(1395, 1005)