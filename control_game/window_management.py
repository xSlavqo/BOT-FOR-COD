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
        time.sleep(1)
        launcher_window = gw.getWindowsWithTitle("launcher")
        while not launcher_window:
            print("Nie znaleziona launchera gry!")
        launcher_window[0].activate()
        if not locate("png/game_start.png", 0.99, 10, True):
            print("Problem z znalezieniem przycisku uruchom!")
        time.sleep(10)
        if not locate("png/city.png", 0.99, 60):
            print("Gra nie chce się załadować!")
    
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
