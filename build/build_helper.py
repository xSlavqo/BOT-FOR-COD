# text_locator.py
import cv2
import numpy as np
import mss
import pytesseract

def text_locator(template_path, target_word):
    # Wczytanie obrazu szablonu z kanałem alfa
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print("Błąd wczytywania szablonu.")
        return True  # Zwróć True, aby wskazać, że nie odnaleziono

    with mss.mss() as sct:
        # Ustawienie monitora na pierwszy dostępny, jeśli monitor o indeksie 2 nie istnieje
        monitor = sct.monitors[2] if len(sct.monitors) > 2 else sct.monitors[1]
        
        # Przechwycenie obrazu ekranu z wybranego monitora
        img = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGRA2BGR)

        # Znajdowanie najlepszego dopasowania
        match_coords = get_best_match_location(img, template)
        found, center_coords = expand_and_extract_text(img, match_coords, target_word)
        
        if found:
            return center_coords
        else:
            return True  # Zwróć True, gdy nie odnaleziono koordynatów

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