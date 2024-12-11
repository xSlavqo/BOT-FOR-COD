# utils/text_recognition.py

import cv2
import numpy as np
import mss
import pytesseract
import re

def capture_and_read_text(area):
    with mss.mss() as sct:
        monitor = {"top": area[1], "left": area[0], "width": area[2] - area[0], "height": area[3] - area[1]}
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    gray_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    tesseract_result = pytesseract.image_to_string(binary_image).replace('\n', ' ').replace('\t', ' ')
    tesseract_result = re.sub(r'\s+', '', tesseract_result)  # Usunięcie wszystkich białych znaków

    time_pattern = r"\d{1,2}:\d{2}:\d{2}"
    time_match = re.search(time_pattern, tesseract_result)
    
    if not time_match:
        print(f"OCR result: '{tesseract_result}' — Nie znaleziono czasu.")
        return "Not Found"
    
    return time_match.group(0).strip()


if __name__ == "__main__":
    aha = capture_and_read_text((1335, 878, 1475, 913))
    print(aha)