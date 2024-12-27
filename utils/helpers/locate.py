# utils.locate.py
import cv2
import numpy as np
import mss
import time
import pyautogui
import random

def is_image_match(img, template, threshold):
    base = template[:, :, :3]
    alpha_mask = cv2.merge([template[:, :, 3]] * 3)
    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha_mask)
    max_val = correlation.max()
    matches = list(zip(*np.where(correlation >= threshold)[::-1]))
    return matches, max_val

def locate(template_path, threshold, max_time=5, click_center=False):
    # Wczytanie obrazu szablonu z kanałem alfa
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    start_time = time.time()
    
    with mss.mss() as sct:
        # Ustawienie monitora na pierwszy dostępny, jeśli monitor o indeksie 2 nie istnieje
        monitor = sct.monitors[2] if len(sct.monitors) > 2 else sct.monitors[1]
        
        while time.time() - start_time < max_time:
            screen_shot = sct.grab(monitor)
            img = np.array(screen_shot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            matches, _ = is_image_match(img, template, threshold)
            if matches:
                if click_center:
                    # Dodanie losowej zwłoki przed kliknięciem
                    time.sleep(random.uniform(0.5, 1.5))
                    center_x = matches[0][0] + template.shape[1] // 2
                    center_y = matches[0][1] + template.shape[0] // 2
                    pyautogui.click(center_x + monitor["left"], center_y + monitor["top"])
                
                # Losowe opóźnienie od 1.5 do 3 sekund
                time.sleep(random.uniform(0.7, 1.6))
                return True

    return False


if __name__ == "__main__":
    result = locate("stay/stay.png", 0.99, 5, False)
    print(f"Obraz znaleziony: {result}")
