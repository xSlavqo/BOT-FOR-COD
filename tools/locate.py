import pyautogui
import cv2
import numpy as np
import os

def is_image_match(img, template, threshold):
    hh, ww = template.shape[:2]
    base = template[:, :, 0:3]
    alpha = template[:, :, 3]
    alpha = cv2.merge([alpha, alpha, alpha])

    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha)
    loc = np.where(correlation >= threshold)

    matches = list(zip(*loc[::-1]))
    return len(matches) >= 1

def locate(path, threshold):
    img = pyautogui.screenshot()
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                template = cv2.imread(os.path.join(path, filename), cv2.IMREAD_UNCHANGED)
                if is_image_match(img, template, threshold):
                    return True
        return False
    elif os.path.isfile(path) and path.endswith(".png"):
        template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        return is_image_match(img, template, threshold)
    else:
        return False

def locate_and_click(path, threshold):
    img = pyautogui.screenshot()
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

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
                        pyautogui.click(center)
                        return True
        return False
    elif os.path.isfile(path) and path.endswith(".png"):
        template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if is_image_match(img, template, threshold):
            hh, ww = template.shape[:2]
            loc = np.where(cv2.matchTemplate(img, template[:, :, 0:3], cv2.TM_CCORR_NORMED, mask=template[:, :, 3]) >= threshold)
            if len(loc[0]) > 0:
                pt = (loc[1][0], loc[0][0])
                center = (pt[0] + ww // 2, pt[1] + hh // 2)
                pyautogui.click(center)
                return True
        return False
    else:
        return False

def locate_numbers(path, threshold):
    img = pyautogui.screenshot()
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    count = 0  # Zmienna do przechowywania łącznej liczby dopasowań

    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                template = cv2.imread(os.path.join(path, filename), cv2.IMREAD_UNCHANGED)
                count += is_image_match(img, template, threshold)
    elif os.path.isfile(path) and path.endswith(".png"):
        template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        count = is_image_match(img, template, threshold) 

    return count  # Zwróć całkowitą liczbę znalezionych dopasowań

