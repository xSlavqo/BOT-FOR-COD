import re
import pyautogui
import time
from datetime import datetime, timedelta
from tasks.location import *
from tools.locate import *
from tools.text import *


def check_pd():
    while not locate_and_click("pngs/PD_points.png", 0.99):
        pyautogui.press("esc")
    pd = text((199, 343, 94, 25), invert_colors=0, tolerance=240, blur_ksize=1)
    print(pd)
    if '/' in pd:
        licznik, mianownik = pd.split('/')
        licznik = int(licznik.replace(' ', '').replace('\n', '').strip())
        mianownik = int(mianownik.replace(' ', '').replace('\n', '').strip())
        procent = (licznik / mianownik) * 100
        print(f"Postęp: {procent:.2f}%")
    time.sleep(1)
    pd = text((99, 548, 345, 41), invert_colors=1, tolerance=240, blur_ksize=1)
    print(pd)
check_pd()