import cv2
from PIL import Image, ImageGrab
import pytesseract
import numpy as np

def text(region):
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    gray_image = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    x, y, w, h = region
    region_image = gray_image[y:y+h, x:x+w]
    region_pil = Image.fromarray(region_image)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(region_pil, lang='pol', config=custom_config)
    return text


if __name__ == "__main__":
    aha = text((1, 1, 1919, 850))
    print (aha)