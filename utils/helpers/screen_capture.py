# utils/screen_capture.py

import cv2
import numpy as np
import mss

def capture_and_select_areas():
    with mss.mss() as sct:
        monitor = sct.monitors[2]
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    # Umożliw zaznaczenie wielu regionów
    rois = cv2.selectROIs("Select Areas", screenshot, showCrosshair=True)
    cv2.destroyAllWindows()

    if len(rois) > 0:
        areas = []
        for roi in rois:
            x, y, w, h = roi
            if w > 0 and h > 0:
                areas.append((x, y, w, h))
        print(f"Selected areas: {areas}")
        return areas
    else:
        print("No areas selected.")
        return None

# Przykład użycia
if __name__ == "__main__":
    capture_and_select_areas()
