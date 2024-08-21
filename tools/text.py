import cv2
from PIL import ImageGrab
import pytesseract
import numpy as np

def text(region, invert_colors=0, tolerance=254, blur_ksize=3):
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    gray_image = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    x, y, w, h = region
    region_image = gray_image[y:y+h, x:x+w]

    if invert_colors == 1:
        # Zamiana nie-białych pikseli na czarne
        mask = region_image < tolerance
        region_image[mask] = 0
        region_image[~mask] = 255
        
        # Odwrócenie kolorów
        region_image = cv2.bitwise_not(region_image)
        
        # Wygładzenie krawędzi za pomocą rozmycia Gaussowskiego
        region_image = cv2.GaussianBlur(region_image, (blur_ksize, blur_ksize), 0)

    # Przetwarzanie OCR bezpośrednio na obrazie
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(region_image, lang='pol', config=custom_config)
    return text

if __name__ == "__main__":
    aha = text((1157, 320, 46, 25), invert_colors=1, tolerance=240, blur_ksize=1)
    print(aha)
