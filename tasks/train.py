import time
from tools.locate import locate_and_click
from tasks.location import *

def train(unit_type):
    city()
    time.sleep(1)  
    locate_and_click(f"pngs/units/{unit_type}/place.png", 0.99, 0, 0, 10)
    time.sleep(1)  
    if locate_and_click("pngs/units/speed.png", 0.99, 0, 0, 10):
        return True
    return False

train("inf")