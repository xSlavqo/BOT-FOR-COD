# train_helper.py
import cv2
import numpy as np
import mss
import pygetwindow as gw
import pyautogui
import os
from screeninfo import get_monitors

def train_helper(folder_path, threshold=0.8):
    # Znajdowanie okna Call of Dragons
    windows = gw.getWindowsWithTitle("Call of Dragons")
    if not windows:
        print("Okno 'Call of Dragons' nie zostało znalezione.")
        return False

    # Pobranie okna i jego współrzędnych
    window = windows[0]
    win_x, win_y = window.left, window.top
    win_w, win_h = window.width, window.height

    with mss.mss() as sct:
        # Znalezienie monitora, na którym jest okno
        monitor = None
        for mon in get_monitors():
            if mon.x <= win_x < mon.x + mon.width and mon.y <= win_y < mon.y + mon.height:
                monitor = {"top": win_y, "left": win_x, "width": win_w, "height": win_h}
                break
        
        if not monitor:
            print("Nie znaleziono odpowiedniego monitora dla okna.")
            return False

        # Przechwycenie obrazu ekranu z wybranego monitora
        img = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2BGR)

        # Przeszukiwanie folderu z obrazami
        for filename in os.listdir(folder_path):
            template_path = os.path.join(folder_path, filename)
            template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
            if template is None:
                print(f"Błąd wczytywania szablonu: {filename}")
                continue

            match_coords = get_best_match_location(img, template, threshold)
            if match_coords:
                # Oblicz współrzędne kliknięcia (40 pikseli poniżej środka dopasowania)
                center_x, center_y = match_coords
                click_x, click_y = center_x, center_y + 80
                # Wykonaj kliknięcie
                pyautogui.mouseDown(click_x, click_y)
                pyautogui.mouseUp(click_x, click_y)
                return True
        
        print("Nie znaleziono żadnego dopasowania.")
        return False

def get_best_match_location(img, template, threshold):
    # Dopasowanie obrazu
    base, mask = template[:, :, :3], cv2.merge([template[:, :, 3]] * 3)
    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(correlation)

    if max_val >= threshold:
        # Znaleziono dopasowanie powyżej progu
        x, y = max_loc
        center_x, center_y = x + template.shape[1] // 2, y + template.shape[0] // 2
        return center_x, center_y

    return None


