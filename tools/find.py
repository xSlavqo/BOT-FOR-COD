import cv2
import numpy as np
import os
import pyautogui
import random

def main(path):
    images = []
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                img = cv2.imread(os.path.join(path, filename))
                if img is not None:
                    images.append(img)
    elif os.path.isfile(path) and path.endswith(".png"):
        img = cv2.imread(path)
        if img is not None:
            images.append(img)

    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    sift = cv2.SIFT_create()
    screenshot_kp, screenshot_desc = sift.detectAndCompute(screenshot, None)
    
    return images, screenshot, sift, screenshot_kp, screenshot_desc

def find(path, threshold, min_matches):
    images, screenshot, sift, screenshot_kp, screenshot_desc = main(path)
    index_params = dict(algorithm=1, trees=5)
    flann = cv2.FlannBasedMatcher(index_params, dict())

    for img in images:
        kp, desc = sift.detectAndCompute(img, None)
        matches = flann.knnMatch(desc, screenshot_desc, k=2)
        good_matches = [m for m, n in matches if m.distance < threshold * n.distance]
        if len(good_matches) >= min_matches:
            return True
    return False

def find_and_click(path, threshold, min_matches):
    images, screenshot, sift, screenshot_kp, screenshot_desc = main(path)
    index_params = dict(algorithm=1, trees=5)
    flann = cv2.FlannBasedMatcher(index_params, dict())

    for img in images:
        kp, desc = sift.detectAndCompute(img, None)
        matches = flann.knnMatch(desc, screenshot_desc, k=2)
        good_matches = [m for m, n in matches if m.distance < threshold * n.distance]
        if len(good_matches) >= min_matches:
            chosen_match = random.choice(good_matches)
            point = screenshot_kp[chosen_match.trainIdx].pt
            x, y = int(point[0]), int(point[1])
            pyautogui.click(x, y)
            return True
    return False

def find_numbers(path, threshold, min_matches):
    images, screenshot, sift, screenshot_kp, screenshot_desc = main(path)
    index_params = dict(algorithm=1, trees=5)
    flann = cv2.FlannBasedMatcher(index_params, dict())
    available_images_count = 0

    for img in images:
        kp, desc = sift.detectAndCompute(img, None)
        matches = flann.knnMatch(desc, screenshot_desc, k=2)
        good_matches = [m for m, n in matches if m.distance < threshold * n.distance]
        if len(good_matches) >= min_matches:
            available_images_count += 1

    return available_images_count

