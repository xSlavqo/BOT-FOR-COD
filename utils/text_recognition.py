# utils/text_recognition.py

import cv2
import numpy as np
import mss
import pytesseract
import easyocr
import re

def capture_and_read_text(area):
    with mss.mss() as sct:
        monitor = {"top": area[1], "left": area[0], "width": area[2] - area[0], "height": area[3] - area[1]}
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    # Binaryzacja obrazu
    gray_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    # Odwrócenie kolorów
    inverted_image = cv2.bitwise_not(binary_image)

    # Wyświetlenie obrazu po odwróceniu kolorów
    cv2.imshow("Inverted Binary Image", inverted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # EasyOCR
    reader = easyocr.Reader(['pl'], gpu=False)
    easyocr_result = reader.readtext(inverted_image, detail=0)
    easyocr_text = " ".join(easyocr_result).replace(".", ":")

    # Tesseract
    tesseract_result = pytesseract.image_to_string(inverted_image, lang='pol').strip()

    # Wyodrębnienie czasu w formacie gg:mm:ss
    time_pattern = r"\b\d{1,2}:\d{2}:\d{2}\b"
    easyocr_time = re.search(time_pattern, easyocr_text)

    easyocr_time = easyocr_time.group(0) if easyocr_time else "Not Found"

# Przykład użycia
if __name__ == "__main__":
    area = (1105, 718, 1390, 741)
    capture_and_read_text(area)
