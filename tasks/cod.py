import pygetwindow as gw
import time
import subprocess
from tools.locate import locate, locate_and_click

program_path = r"C:/Program Files (x86)/Call of Dragons/launcher.exe"

def cod():
    cod_window = gw.getWindowsWithTitle("Call of Dragons")

    if not cod_window:
        subprocess.Popen(program_path)
        launcher_window = gw.getWindowsWithTitle("launcher")
        while not launcher_window:
            launcher_window = gw.getWindowsWithTitle("launcher")
        launcher_window[0].activate()
        while not locate_and_click("pngs/launcher_start.png", 0.99):
            time.sleep(1)
        while not locate("pngs/city", 0.99):
            time.sleep(1)
    
    cod_window = gw.getWindowsWithTitle("Call of Dragons")
    cod_window[0].activate()
    return True

def restart():
    cod_window = gw.getWindowsWithTitle("Call of Dragons")  
    if cod_window:
        cod_window[0].close()
    time.sleep(5)