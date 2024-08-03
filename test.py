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
    # Oddziel kanał alfa, jeśli istnieje
    if image.shape[2] == 4:
        base = image[:, :, 0:3]  # Kanały BGR
        mask = image[:, :, 3].astype(np.uint8)  # Kanał alfa jako maska
    else:
        base = image
        mask = None
    return base, mask

def main(path):
    images = load_images_from_path(path)

    try:
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return [], None, None, None, None

    base, mask = get_base_and_mask(screenshot)
    
    sift = cv2.SIFT_create()
    screenshot_kp, screenshot_desc = sift.detectAndCompute(base, mask=mask)
    
    return images, screenshot, sift, screenshot_kp, screenshot_desc


def find_and_click(path, threshold, min_matches):
    images, screenshot, sift, screenshot_kp, screenshot_desc = main(path)
    
    if not images or screenshot is None:
        print("No images or screenshot available for matching.")
        return False

    index_params = dict(algorithm=1, trees=5)
    flann = cv2.FlannBasedMatcher(index_params, dict())

    for img in images:
        base, mask = get_base_and_mask(img)

        kp, desc = sift.detectAndCompute(base, mask=mask)
        matches = flann.knnMatch(desc, screenshot_desc, k=2)

        good_matches = [m for m, n in matches if m.distance < threshold * n.distance]

        if len(good_matches) >= min_matches:
            chosen_match = random.choice(good_matches)
            point = screenshot_kp[chosen_match.trainIdx].pt
            x, y = int(point[0]), int(point[1])
            pyautogui.click(x, y)
            return True

    print("No sufficient matches found.")
    return False

# Przykład użycia
find_and_click("pngs/units/cav/place.png", 0.8, 5)
