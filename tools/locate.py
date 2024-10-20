import pyautogui
import cv2
import numpy as np
import os
import time

def is_image_match(img, template, threshold):
    hh, ww = template.shape[:2]
    base = template[:, :, 0:3]
    alpha = template[:, :, 3]
    alpha = cv2.merge([alpha, alpha, alpha])
    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha)
    loc = np.where(correlation >= threshold)
    matches = list(zip(*loc[::-1]))
    return len(matches) >= 1

def locate(path, threshold, max_search_time=2):
    end_time = time.time() + max_search_time
    while time.time() < end_time:
        img = pyautogui.screenshot()
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(".png"):
                    template = cv2.imread(os.path.join(path, filename), cv2.IMREAD_UNCHANGED)
                    if is_image_match(img, template, threshold):
                        return True
        elif os.path.isfile(path) and path.endswith(".png"):
            template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if is_image_match(img, template, threshold):
                return True
        time.sleep(0.3) 
    return False

def locate_in_region(path, threshold, region, max_search_time=10):
    end_time = time.time() + max_search_time
    while time.time() < end_time:
        img = pyautogui.screenshot(region=region)
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(".png"):
                    template = cv2.imread(os.path.join(path, filename), cv2.IMREAD_UNCHANGED)
                    if is_image_match(img, template, threshold):
                        return True
        elif os.path.isfile(path) and path.endswith(".png"):
            template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if is_image_match(img, template, threshold):
                return True
        time.sleep(0.3) 
    return False



def locate_and_click(path, threshold, x_offset=0, y_offset=0, max_search_time=2):
    end_time = time.time() + max_search_time
    while time.time() < end_time:
        img = pyautogui.screenshot()
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        def click_with_offset(center):
            offset_center = (center[0] + x_offset, center[1] + y_offset)
            pyautogui.mouseDown(offset_center)
            pyautogui.mouseUp(offset_center) 
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(".png"):
                    template = cv2.imread(os.path.join(path, filename), cv2.IMREAD_UNCHANGED)
                    if is_image_match(img, template, threshold):
                        hh, ww = template.shape[:2]
                        loc = np.where(cv2.matchTemplate(img, template[:, :, 0:3], cv2.TM_CCORR_NORMED, mask=template[:, :, 3]) >= threshold)
                        if len(loc[0]) > 0:
                            pt = (loc[1][0], loc[0][0])
                            center = (pt[0] + ww // 2, pt[1] + hh // 2)
                            click_with_offset(center)
                            return True
        elif os.path.isfile(path) and path.endswith(".png"):
            template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if is_image_match(img, template, threshold):
                hh, ww = template.shape[:2]
                loc = np.where(cv2.matchTemplate(img, template[:, :, 0:3], cv2.TM_CCORR_NORMED, mask=template[:, :, 3]) >= threshold)
                if len(loc[0]) > 0:
                    pt = (loc[1][0], loc[0][0])
                    center = (pt[0] + ww // 2, pt[1] + hh // 2)
                    click_with_offset(center)
                    return True
        time.sleep(0.1)
    return False

def locate_and_click_in_region(path, threshold, region, x_offset=0, y_offset=0, max_search_time=2):
    end_time = time.time() + max_search_time
    while time.time() < end_time:
        img = pyautogui.screenshot(region=region)
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        def click_with_offset(center):
            offset_center = (center[0] + x_offset, center[1] + y_offset)
            pyautogui.mouseDown(offset_center)
            pyautogui.mouseUp(offset_center)
        
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(".png"):
                    template = cv2.imread(os.path.join(path, filename), cv2.IMREAD_UNCHANGED)
                    if is_image_match(img, template, threshold):
                        hh, ww = template.shape[:2]
                        loc = np.where(cv2.matchTemplate(img, template[:, :, 0:3], cv2.TM_CCORR_NORMED, mask=template[:, :, 3]) >= threshold)
                        if len(loc[0]) > 0:
                            pt = (loc[1][0], loc[0][0])
                            center = (pt[0] + ww // 2, pt[1] + hh // 2)
                            click_with_offset((center[0] + region[0], center[1] + region[1]))  # Dodaj przesunięcie regionu
                            return True
        elif os.path.isfile(path) and path.endswith(".png"):
            template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if is_image_match(img, template, threshold):
                hh, ww = template.shape[:2]
                loc = np.where(cv2.matchTemplate(img, template[:, :, 0:3], cv2.TM_CCORR_NORMED, mask=template[:, :, 3]) >= threshold)
                if len(loc[0]) > 0:
                    pt = (loc[1][0], loc[0][0])
                    center = (pt[0] + ww // 2, pt[1] + hh // 2)
                    click_with_offset((center[0] + region[0], center[1] + region[1]))  # Dodaj przesunięcie regionu
                    return True
        time.sleep(0.1)
    return False
