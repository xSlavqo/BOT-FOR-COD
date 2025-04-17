from utils.helpers.locate import locate
import pyautogui
import time

def chests():
    locate("chests/1.png", 0.99, 20, True)
    pyautogui.click(1401, 770)
    time.sleep(2)
    pyautogui.click(486, 739)
    locate("chests/2.png", 0.99, 20, True)