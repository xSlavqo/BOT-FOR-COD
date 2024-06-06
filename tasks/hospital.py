import pyautogui
from tools.locate import *
from tasks.location import *


def hospital():
    city()
    time.sleep(1)
    if locate_and_click("pngs/hospital.png", 0.95):
        time.sleep(1)
        locate_and_click("pngs/heal.png", 0.99)
        time.sleep(1)
        pyautogui.press("esc")