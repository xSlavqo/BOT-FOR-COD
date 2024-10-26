# window_management.py

import pygetwindow as gw
import time
import subprocess
from utils.locate import *

program_path = r"C:/Program Files (x86)/Call of Dragons/launcher.exe"

def cod_run():
    cod_window = gw.getWindowsWithTitle("Call of Dragons")

    if not cod_window:
        subprocess.Popen(program_path)
        launcher_window = gw.getWindowsWithTitle("launcher")
        while not launcher_window:
            launcher_window = gw.getWindowsWithTitle("launcher")
        launcher_window[0].activate()
        while not locate("pngs/game_start.png", 0.99, 10):
            time.sleep(1)
        while not locate("pngs/city", 0.99):
            time.sleep(1)
    
    cod_window = gw.getWindowsWithTitle("Call of Dragons")
    cod_window[0].activate()
    return True

def cod_restart():
    cod_window = gw.getWindowsWithTitle("Call of Dragons")  
    while cod_window:
        cod_window[0].close()
        time.sleep(1)
        cod_window = gw.getWindowsWithTitle("Call of Dragons")

def tv_close():
    tv_window = gw.getWindowsWithTitle("Sesja sponsorowana")
    while tv_window:
        tv_window[0].close()
        time.sleep(1)
        tv_window = gw.getWindowsWithTitle("Sesja sponsorowana")
