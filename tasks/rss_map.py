import time
import pyautogui
import random
import pyautogui
import re
import pytesseract
from tasks.cod import cod
from tools.locate import *
from tasks.legions import legions
from tasks.location import *
from tools.functions import load_config
from tools.find import *
from PIL import Image

def rss_map():
    for _ in range(check_legions()):
        map()
        time.sleep(1)
        pyautogui.press("f")
        time.sleep(1)
        rss_type()
        time.sleep(0.5)
        #rss_level()
        time.sleep(0.5)
        locate_and_click("pngs/rss_find.png", 0.99)
        pyautogui.moveTo(1, 1)
        time.sleep(2)
        if locate("pngs/rss_find.png", 0.99):
            pyautogui.press("esc")
            continue
        pyautogui.mouseDown(960, 540)
        pyautogui.mouseUp(960, 540) 
        time.sleep(0.2)
        pyautogui.mouseDown(960, 540)
        pyautogui.mouseUp(960, 540)
        time.sleep(1)
        if not locate_and_click("pngs/rss_gather.png", 0.99):
            continue
        time.sleep(1)
        if not locate_and_click("pngs/make_legion.png", 0.99):
            pyautogui.press("esc")
            continue
        time.sleep(1)
        locate_and_click("pngs/one_hero.png", 0.99)
        time.sleep(1)
        locate_and_click("pngs/march.png", 0.99)
        time.sleep(1)
    


def check_legions():
    max_gathers = int(load_config().get('max_gathers'))
    on_map = int(legions())
    difference = max_gathers - on_map
    return difference



def rss_type():
    config = load_config()
    selected_resources = []
    if config.get("gold"):
        selected_resources.append(1)
    if config.get("wood"):
        selected_resources.append(2)
    if config.get("stone"):
        selected_resources.append(3)
    if config.get("mana"):
        selected_resources.append(4)
    if not selected_resources:
        selected_resources = [1, 2, 3, 4]
    selected_option = random.choice(selected_resources)
    if selected_option == 1:
        pyautogui.click(735, 1005)
    elif selected_option == 2:
        pyautogui.click(955, 1005)
    elif selected_option == 3:
        pyautogui.click(1175, 1005)
    elif selected_option == 4:
        pyautogui.click(1395, 1005)


def rss_level():
    config = load_config()
    rss_level = int(config.get('rss_level'))

    screenshot = pyautogui.screenshot()
    text = pytesseract.image_to_string(screenshot)
    search_pattern = "Poziom//s(//d+)"
    search_results = re.search(search_pattern, text)
    actually_rss_level = int(search_results.group(1))
    level_focus = rss_level - actually_rss_level
    if level_focus > 0:
        for i in range(level_focus):
            locate_and_click("pngs/lvladd.png", 0.99)
            time.sleep(0.5)
    elif level_focus < 0:
        for i in range(abs(level_focus)):
            locate_and_click("pngs/lvlreduce.png", 0.99)
            time.sleep(0.5)
