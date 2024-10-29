# auto_build.py
import pyautogui
from build.build_helper import text_locator
from utils.locate import locate

def auto_build():
    if (coords := text_locator("png/build/build1.png", "buduj")):
        pyautogui.mouseDown(coords[0], coords[1] + 40); pyautogui.mouseUp()
        locate("png/build/build2.png", 0.95, 5, True)
        locate("png/build/build3.png", 0.95, 5, True)
        if not locate ("png/build/build4.png", 0.99, 5, True):
            pyautogui.mouseDown(292, 792); pyautogui.mouseUp(292, 792)
            locate("png/build/build_new.png", 0.95, 5, True)  
        else:
            locate("png/build/build4.png", 0.95, 5, True)
            locate("png/build/build5.png", 0.95, 5, True)
        while not False:
            while locate("png/build/help_ask.png", 0.95, 5, True): return
        