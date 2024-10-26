# locate.py
import cv2
import numpy as np
import mss
import pygetwindow as gw
import time
import pyautogui

def is_image_match(img, template, threshold):
    base = template[:, :, :3]
    alpha_mask = cv2.merge([template[:, :, 3]] * 3)
    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha_mask)
    max_val = correlation.max()
    matches = list(zip(*np.where(correlation >= threshold)[::-1]))
    return matches, max_val

def locate(template_path, threshold, max_time, click_center):
    cod_window = gw.getWindowsWithTitle("Call of Dragons")
    if not cod_window:
        print("Nie znaleziono okna: Call of Dragons")
        return False

    cod_window[0].activate()  # Aktywacja okna

    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    start_time = time.time()
    
    with mss.mss() as sct:
        monitor = {
            "top": cod_window[0].top,
            "left": cod_window[0].left,
            "width": cod_window[0].width,
            "height": cod_window[0].height
        }
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
    result = locate("png/city.png", 0.99, 5, False)
    print(f"Obraz znaleziony: {result}")
