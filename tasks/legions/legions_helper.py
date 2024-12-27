# tasks/legions/legions_helper.py

import cv2
import numpy as np
import mss
import pytesseract
import re
import time
from pygetwindow import getWindowsWithTitle
from screeninfo import get_monitors

def is_image_match(img, template, threshold):
    if template.shape[2] == 4:
        base, alpha_mask = template[:, :, :3], cv2.merge([template[:, :, 3]] * 3)
    else:
        base, alpha_mask = template, None
    
    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha_mask)
    matches = list(zip(*np.where(correlation >= threshold)[::-1]))
    return matches[0] if matches else None

def locate_and_read_legions_status(template_path="png/legions/legions.png", threshold=0.999, max_time=5, offset_x=10, region_width=40, region_height=60):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        return None
    
    windows = getWindowsWithTitle("Call of Dragons")
    if not windows:
        return None

    window = windows[0]
    win_x, win_y = window.left, window.top
    win_w, win_h = window.width, window.height

    with mss.mss() as sct:
        monitor = None
        for mon in get_monitors():
            if mon.x <= win_x < mon.x + mon.width and mon.y <= win_y < mon.y + mon.height:
                monitor = {"top": win_y, "left": win_x, "width": win_w, "height": win_h}
                break
        
        if not monitor:
            return None

        start_time = time.time()
        while time.time() - start_time < max_time:
            screen_shot = sct.grab(monitor)
            img = cv2.cvtColor(np.array(screen_shot), cv2.COLOR_BGRA2BGR)

            match = is_image_match(img, template, threshold)
            if match:
                center_x, center_y = match[0] + template.shape[1] // 2, match[1] + template.shape[0] // 2
                fragment = img[max(center_y - region_height // 2, 0):min(center_y + region_height // 2, img.shape[0]),
                               max(center_x + offset_x, 0):min(center_x + offset_x + region_width, img.shape[1])]

                text = pytesseract.image_to_string(fragment).strip()
                if match := re.match(r"(\d)/(\d)", text):
                    return int(match.group(2)) - int(match.group(1))
                
                return 1

    return None
