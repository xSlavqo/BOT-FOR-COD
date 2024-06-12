import time
import pyautogui
from tasks.location import city
from tools.locate import locate_in_time

def dialogues():
    city()
    if locate_in_time("pngs\dialogues/test.png", 0.9999, 50, 5):
        time.sleep(1)
        if locate_in_time("pngs/dialogues.png", 0.99,50 ,5):
            time.sleep(1)
            pyautogui.click(1847, 40)
            time.sleep(1)
            pyautogui.press("esc")
            time.sleep(0.5)
            dialogues()