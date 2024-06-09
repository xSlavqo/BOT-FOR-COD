import time
import pyautogui
import re
from tasks.location import *
from tools.locate import *
from tools.text import text

def legions_menu():
    if not locate("pngs/legions.png", 0.995):
        main_screen()
        pyautogui.press("j")
        time.sleep(1)
        if not locate("pngs/legions.png", 0.995):
            return False
    return True

def legions():
    if legions_menu():
        time.sleep(1)
        raw_text = text((1667, 1, 114, 55))
        match = re.search(r'(\d)/', raw_text)
        legions_count = match.group(1) if match else None
        return legions_count
    return 0
