# window_management.py

import pygetwindow as gw
import time
import subprocess
from utils.helpers.locate import *

program_path = r"C:/Program Files (x86)/Call of Dragons/launcher.exe"

def cod_run():
    cod_window = gw.getWindowsWithTitle("Call of Dragons")
    max_launcher_attempts = 5
    
    if not cod_window:
        subprocess.Popen(program_path)
        time.sleep(10)
        
        launcher_window = gw.getWindowsWithTitle("launcher")
        launcher_attempts = 0
        while not launcher_window and launcher_attempts < max_launcher_attempts:
            print("Nie odnaleziono launchera gry!")
            launcher_attempts += 1
            time.sleep(2)
            launcher_window = gw.getWindowsWithTitle("launcher")
        
        if not launcher_window:
            print("Problem z uruchomieniem launchera gry.")
            return False

        launcher_window[0].activate()
        
        if not locate("png/game_start.png", 0.99, 10, True):
            print("Problem z odnalezieniem przycisku uruchom!")
            return False

        time.sleep(10)
        if not locate("png/city.png", 0.99, 60):
            print("Gra nie chce się załadować!")
            return False
    
    cod_window = gw.getWindowsWithTitle("Call of Dragons")
    cod_window[0].activate()
    return True

def cod_restart():
    max_close_attempts = 5
    cod_window = gw.getWindowsWithTitle("Call of Dragons")
    
    while cod_window:
        close_attempts = 0
        while close_attempts < max_close_attempts and cod_window:
            cod_window[0].close()
            time.sleep(1)
            cod_window = gw.getWindowsWithTitle("Call of Dragons")
            close_attempts += 1
        
        if cod_window:
            print("Nie udało się zamknąć okna gry.")
            return False
    
    return True

def tv_close():
    max_close_attempts = 5
    tv_window = gw.getWindowsWithTitle("Sesja sponsorowana")
    
    while tv_window:
        close_attempts = 0
        while close_attempts < max_close_attempts and tv_window:
            tv_window[0].close()
            time.sleep(1)
            tv_window = gw.getWindowsWithTitle("Sesja sponsorowana")
            close_attempts += 1
        
        if tv_window:
            print("Nie udało się zamknąć okna Sesja sponsorowana.")
            return False
    
    return True
