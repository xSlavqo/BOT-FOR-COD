import cv2
import numpy as np
import mss
import pytesseract
import re
import pygetwindow as gw

def find_call_of_dragons_monitor():
    try:
        window = gw.getWindowsWithTitle('Call of Dragons')[0]
        window_x, window_y = window.left, window.top

        with mss.mss() as sct:
            for index, monitor in enumerate(sct.monitors[1:], start=1):
                mon_left = monitor['left']
                mon_top = monitor['top']
                mon_width = monitor['width']
                mon_height = monitor['height']

                if (mon_left <= window_x < mon_left + mon_width) and (mon_top <= window_y < mon_top + mon_height):
                    return index

        raise Exception("Nie znaleziono monitora z Call of Dragons")
    except IndexError:
        raise Exception("Nie znaleziono okna Call of Dragons")

def text_recognition(region_coordinates):
    try:
        monitor_index = find_call_of_dragons_monitor()
        
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(sct.monitors[monitor_index]))
        
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
        return None
    
    except Exception as e:
        return None

if __name__ == "__main__":
    print(text_recognition((1149, 705, 218, 48)))
