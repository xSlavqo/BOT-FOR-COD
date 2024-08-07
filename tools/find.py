import cv2
import numpy as np
import os
import pyautogui
import random

def load_images_from_path(path):
    images = []
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                img = cv2.imread(os.path.join(path, filename), cv2.IMREAD_UNCHANGED)
                if img is not None:
                    images.append(img)
    elif os.path.isfile(path) and path.endswith(".png"):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is not None:
            images.append(img)
    return images

def get_base_and_mask(image):
    if image.shape[2] == 4:
        base = image[:, :, :3]
        mask = image[:, :, 3].astype(np.uint8)
    else:
        base = image
        mask = None
    return base, mask

def main(path):
    images = load_images_from_path(path)
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    base, mask = get_base_and_mask(screenshot)
    sift = cv2.SIFT_create()
    screenshot_kp, screenshot_desc = sift.detectAndCompute(base, mask=mask)
    return images, screenshot_kp, screenshot_desc, sift

def find_and_click(path, threshold, min_matches):
    images, screenshot_kp, screenshot_desc, sift = main(path)
    index_params = dict(algorithm=1, trees=5)
    flann = cv2.FlannBasedMatcher(index_params, {})

    for img in images:
        base, mask = get_base_and_mask(img)
        kp, desc = sift.detectAndCompute(base, mask=mask)
        matches = flann.knnMatch(desc, screenshot_desc, k=2)
        good_matches = [m for m, n in matches if m.distance < threshold * n.distance]

        if len(good_matches) >= min_matches:
            chosen_match = random.choice(good_matches)
            x, y = screenshot_kp[chosen_match.trainIdx].pt
            offset_center = (int(x), int(y))
            pyautogui.mouseDown(offset_center)
            pyautogui.mouseUp(offset_center)
            return True
    return False