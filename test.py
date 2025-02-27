# main_module.py
import cv2
import pyautogui
import numpy as np
import math
import easyocr

def find_seed(img):
    h, w = img.shape
    cx, cy = w // 2, h // 2
    if img[cy, cx] == 0:
        return (cx, cy)
    for r in range(1, min(cx, cy)):
        for theta in np.linspace(0, 2 * math.pi, 36, endpoint=False):
            x = int(cx + r * math.cos(theta))
            y = int(cy + r * math.sin(theta))
            if 0 <= x < w and 0 <= y < h and img[y, x] == 0:
                return (x, y)
    return (cx, cy)

def process_region(region):
    region_scaled = cv2.resize(region, None, fx=10, fy=10, interpolation=cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(region_scaled, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 50, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    inverted = cv2.bitwise_not(mask)
    seed = find_seed(inverted)
    h_i, w_i = inverted.shape
    flood_copy = inverted.copy()
    mask_fill = np.zeros((h_i + 2, w_i + 2), np.uint8)
    cv2.floodFill(flood_copy, mask_fill, seed, 128)
    final = np.where(flood_copy == 128, 0, 255).astype(np.uint8)
    return region_scaled, final

def main():
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    selected_areas = [
        (1820, 202, 29, 27),
        (1794, 279, 29, 35),
        (1782, 360, 24, 33),
        (1768, 439, 32, 32),
        (1772, 522, 27, 28)
    ]
    whitelist = "QWERTqwert"
    reader = easyocr.Reader(['en'], gpu=False)
    total_letters = 0
    for i, (x, y, w, h) in enumerate(selected_areas):
        region = img[y:y+h, x:x+w]
        _, final = process_region(region)
        result = reader.readtext(final, allowlist=whitelist, detail=1)
        if result:
            # Usuń spacje, aby zliczyć tylko litery
            detected_text = result[0][1].replace(" ", "")
            count = len(detected_text)
        else:
            count = 0
        total_letters += count
        print(f"Region {i+1}: wykryto {count} liter")
    print(f"Łącznie wykryto {total_letters} liter")

if __name__ == "__main__":
    main()
