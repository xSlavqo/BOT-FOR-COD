import pyautogui
import time
import re
from tools.locate import locate, locate_and_click
from tasks.location import city, map
from tools.text import text

def check_lvl(building):
    city()
    pyautogui.mouseDown(x=building.position_x, y=building.position_y)
    pyautogui.mouseUp(x=building.position_x, y=building.position_y)
    if not locate(f'pngs/building/{building.name}.png', 0.95):
        city()
        map()
        pyautogui.mouseDown(x=building.position_x, y=building.position_y)
        pyautogui.mouseUp(x=building.position_x, y=building.position_y)
    locate_and_click("pngs/info.png", 0.95)
    time.sleep(1)
    info = text((987, 529, 427, 66), invert_colors=0, tolerance=240, blur_ksize=1)
    match = re.search(r'Poziom\s(\d+)', info)
    building.level = int(match.group(1))
    return building.level