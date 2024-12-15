# utils/text_recognition.py

import cv2
import numpy as np
import mss
import pytesseract
import re

def text_recognition(region_coordinates):
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(sct.monitors[2]))
    
    x, y, width, height = region_coordinates
    region = screenshot[y:y+height, x:x+width]  
    
    gray_region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    height, width = gray_region.shape
    gray_region = cv2.resize(gray_region, (width * 5, height * 5), interpolation=cv2.INTER_LINEAR)
    
    tesseract_result = pytesseract.image_to_string(gray_region)
    time_pattern = r"\b\d{1,2}:\d{2}:\d{2}\b"
    time_match = re.search(time_pattern, tesseract_result)
    
    if time_match:
        return time_match.group(0)

if __name__ == "__main__":
    print(text_recognition((1274, 875, 233, 42)))
