# locate.py
import cv2
import numpy as np
import mss
import time
import pyautogui

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
        monitor = sct.monitors[2]  # Ustawienie na cały pierwszy monitor
        while time.time() - start_time < max_time:
            screen_shot = sct.grab(monitor)
            img = np.array(screen_shot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            matches, _ = is_image_match(img, template, threshold)
            if matches:
                if click_center:
                    center_x = matches[0][0] + template.shape[1] // 2
                    center_y = matches[0][1] + template.shape[0] // 2
                    pyautogui.click(center_x + monitor["left"], center_y + monitor["top"])
                return True

    return False

if __name__ == "__main__":
    result = locate("stay/stay.png", 0.99, 5, False)
    print(f"Obraz znaleziony: {result}")
