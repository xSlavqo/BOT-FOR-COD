# utils/screen_capture.py

import cv2
import numpy as np
import mss

def capture_and_select_area():
    with mss.mss() as sct:
        monitor = sct.monitors[2]
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
    
    roi = cv2.selectROI("Select Area", screenshot, showCrosshair=True)
    cv2.destroyAllWindows()

    if roi[2] > 0 and roi[3] > 0:
        x, y, w, h = roi
        area = (x, y, x + w, y + h)
        print(f"Selected area: {area}")
        return area
    else:
        print("No area selected.")
        return None

# Przykład użycia
if __name__ == "__main__":
    capture_and_select_area()
