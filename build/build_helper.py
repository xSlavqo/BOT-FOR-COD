# text_locator.py
import cv2
import numpy as np
import mss
import pytesseract
import pygetwindow as gw
import pyautogui
from screeninfo import get_monitors

def text_locator(template_path, target_word):
    # Wczytanie obrazu szablonu z kanałem alfa
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print("Błąd wczytywania szablonu.")
        return False

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

        # Znajdowanie najlepszego dopasowania
        match_coords = get_best_match_location(img, template)
        found, center_coords = expand_and_extract_text(img, match_coords, target_word)
        
        if found:
            # Oblicz współrzędne kliknięcia (40 pikseli poniżej środka dopasowania)
            click_x, click_y = center_coords[0], center_coords[1] + 40
            # Wykonaj kliknięcie
            pyautogui.mouseDown(click_x, click_y)
            pyautogui.mouseUp(click_x, click_y)
            pyautogui.mouseDown(click_x, click_y)
            pyautogui.mouseUp(click_x, click_y)
            return True
        else:
            return False

def get_best_match_location(img, template):
    base, mask = template[:, :, :3], cv2.merge([template[:, :, 3]] * 3)
    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=mask)
    max_loc = np.unravel_index(np.argmax(correlation), correlation.shape)
    x, y = max_loc[::-1]
    return x, y, template.shape[1], template.shape[0]

def expand_and_extract_text(img, match_coords, target_word, expand_ratio=0.2):
    x, y, w, h = match_coords
    ex, ey = int(expand_ratio * w), int(expand_ratio * h)
    roi = img[max(0, y - ey):min(img.shape[0], y + h + ey), max(0, x - ex):min(img.shape[1], x + w + ex)]
    text = pytesseract.image_to_string(roi, lang='eng', config='--psm 6').strip()

    # Sprawdzenie, czy znaleziony tekst zawiera szukane słowo
    if target_word.lower() in text.lower():
        center = (x + w // 2, y + h // 2)
        return True, center
    return False, None
