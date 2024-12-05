# utils/text_recognition.py

import cv2
import numpy as np
import mss
import pytesseract
import re

def capture_and_read_text(area):
    # Pobranie fragmentu ekranu
    with mss.mss() as sct:
        monitor = {"top": area[1], "left": area[0], "width": area[2] - area[0], "height": area[3] - area[1]}
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    # Konwersja do skali szarości i binaryzacja
    gray_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    # Odwrócenie kolorów
    inverted_image = cv2.bitwise_not(binary_image)

    # Odczyt tekstu za pomocą Tesseract
    tesseract_result = pytesseract.image_to_string(inverted_image, lang='pol').strip()

    # Wyodrębnienie czasu w formacie gg:mm:ss
    time_pattern = r"\b\d{1,2}:\d{2}:\d{2}\b"
    time_match = re.search(time_pattern, tesseract_result)
    print(time_match)

    # Zwracanie odczytanego czasu lub "Not Found"
    return time_match.group(0) if time_match else "Not Found"

if __name__ == "__main__":
    capture_and_read_text((1335, 878, 1475, 913))