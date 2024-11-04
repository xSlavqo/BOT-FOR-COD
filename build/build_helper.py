# text_locator.py
import cv2
import numpy as np
import mss
import pygetwindow as gw
import pytesseract

def text_locator(template_path, target_word):
    game_window = gw.getWindowsWithTitle("Call of Dragons")
    if not game_window:
        print("Nie znaleziono okna gry.")
        return None

    game_window[0].activate()
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print("Błąd wczytywania szablonu.")
        return None

    with mss.mss() as sct:
        monitor = {"top": game_window[0].top, "left": game_window[0].left,
                   "width": game_window[0].width, "height": game_window[0].height}
        img = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2BGR)

        match_coords = get_best_match_location(img, template)
        found, center_coords = expand_and_extract_text(img, match_coords, target_word)
        
        if found:
            print(f"Znaleziono dopasowanie! Środek: {center_coords}") 
            return center_coords
        else:
            print("Nie znaleziono dopasowania z podanym słowem.")
            return None

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

    if text.lower() == target_word.lower():
        center = (x + w // 2, y + h // 2)
        return True, center
    return False, None
