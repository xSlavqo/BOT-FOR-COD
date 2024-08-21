from tasks.location import *
from tools.locate import *

def load_building_coordinates():
    coordinates = {}
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "buildings.txt")
    
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            unit = lines[i].split('_')[0]
            x = int(lines[i].split('=')[1].strip())
            y = int(lines[i+1].split('=')[1].strip())
            coordinates[unit] = (x, y)
    
    return coordinates

def build():
    coordinates = load_building_coordinates()
    city()
    time.sleep(1)
    x, y = coordinates["building"]
    pyautogui.mouseDown(x, y)
    time.sleep(0.1)
    pyautogui.mouseUp(x, y)
    time.sleep(1)


build()