import cv2
import numpy as np
import mss
import time
from datetime import datetime

def is_image_match(img, template, threshold):
    # Using template matching with correlation
    base = template[:, :, :3]
    alpha_mask = cv2.merge([template[:, :, 3]] * 3) if template.shape[2] == 4 else None
    method = cv2.TM_CCOEFF_NORMED if alpha_mask is None else cv2.TM_CCORR_NORMED
    correlation = cv2.matchTemplate(img, base, method, mask=alpha_mask)
    max_val = correlation.max()
    matches = list(zip(*np.where(correlation >= threshold)[::-1]))
    return matches, max_val

def continuous_locate(template_path, threshold):
    # Load template image with alpha channel
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

    if template is None:
        print("Error: Template image could not be loaded.")
        return

    with mss.mss() as sct:
        # Set monitor to the second one if available, otherwise use the first
        monitor = sct.monitors[2] if len(sct.monitors) > 2 else sct.monitors[1]

        while True:
            screen_shot = sct.grab(monitor)
            img = np.array(screen_shot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            matches, max_val = is_image_match(img, template, threshold)
            if matches:
                for match in matches:
                    center_x = match[0] + template.shape[1] // 2
                    center_y = match[1] + template.shape[0] // 2
                    print(f"[{datetime.now()}] Image found! Match: {max_val:.2f} (Position: {center_x}, {center_y})")
            else:
                print(f"[{datetime.now()}] Image not found! Match: {max_val:.2f}")

if __name__ == "__main__":
    continuous_locate("indis.png", 0.98)
