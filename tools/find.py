import cv2
import numpy as np
import os
import pyautogui
import time
from collections import defaultdict
from scipy.spatial import distance

def load_images_from_path(path, file_extension=".png"):
    images = []
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(file_extension):
                img = cv2.imread(os.path.join(path, filename), cv2.IMREAD_UNCHANGED)
                if img is not None:
                    images.append(img)
    elif os.path.isfile(path) and path.endswith(file_extension):
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

def find_and_click(path, threshold=0.5, min_matches=1, duration=6, iterations_per_second=5, pixel_tolerance=5, offset_x=0, offset_y=0):
    match_counts = defaultdict(list)
    images = load_images_from_path(path)
    sift = cv2.SIFT_create()
    start_time = time.time()

    while (time.time() - start_time) < duration:
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        base, mask = get_base_and_mask(screenshot)
        screenshot_kp, screenshot_desc = sift.detectAndCompute(base, mask=mask)

        index_params = dict(algorithm=1, trees=5)
        flann = cv2.FlannBasedMatcher(index_params, {})

        for img in images:
            base, mask = get_base_and_mask(img)
            kp, desc = sift.detectAndCompute(base, mask=mask)
            if desc is not None and screenshot_desc is not None:
                matches = flann.knnMatch(desc, screenshot_desc, k=2)
                good_matches = [m for m, n in matches if m.distance < threshold * n.distance]

                if len(good_matches) >= min_matches:
                    points = [screenshot_kp[m.trainIdx].pt for m in good_matches]
                    avg_x = int(sum(x for x, y in points) / len(points))
                    avg_y = int(sum(y for x, y in points) / len(points))
                    match_point = (avg_x, avg_y)
                    clustered = False

                    for clustered_point, point_list in match_counts.items():
                        if distance.euclidean(clustered_point, match_point) <= pixel_tolerance:
                            point_list.append(match_point)
                            clustered = True
                            break

                    if not clustered:
                        match_counts[match_point].append(match_point)

        time.sleep(1.0 / iterations_per_second)

    if len(match_counts) > 0:
        best_point, best_cluster = max(match_counts.items(), key=lambda item: len(item[1]))
        centroid_x = int(sum(x for x, y in best_cluster) / len(best_cluster))
        centroid_y = int(sum(y for x, y in best_cluster) / len(best_cluster))
        centroid_point = (centroid_x + offset_x, centroid_y + offset_y)
        pyautogui.mouseDown(centroid_point)
        pyautogui.mouseUp(centroid_point)
        return centroid_point
    
    return None



def find_and_check(path, threshold=0.5, min_matches=1, duration=6, iterations_per_second=5, pixel_tolerance=5):
    match_counts = defaultdict(list)
    images = load_images_from_path(path)
    sift = cv2.SIFT_create()
    start_time = time.time()

    while (time.time() - start_time) < duration:
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        base, mask = get_base_and_mask(screenshot)
        screenshot_kp, screenshot_desc = sift.detectAndCompute(base, mask=mask)

        index_params = dict(algorithm=1, trees=5)
        flann = cv2.FlannBasedMatcher(index_params, {})

        for img in images:
            base, mask = get_base_and_mask(img)
            kp, desc = sift.detectAndCompute(base, mask=mask)
            if desc is not None and screenshot_desc is not None:
                matches = flann.knnMatch(desc, screenshot_desc, k=2)
                good_matches = [m for m, n in matches if m.distance < threshold * n.distance]

                if len(good_matches) >= min_matches:
                    points = [screenshot_kp[m.trainIdx].pt for m in good_matches]
                    avg_x = int(sum(x for x, y in points) / len(points))
                    avg_y = int(sum(y for x, y in points) / len(points))
                    match_point = (avg_x, avg_y)
                    clustered = False

                    for clustered_point, point_list in match_counts.items():
                        if distance.euclidean(clustered_point, match_point) <= pixel_tolerance:
                            point_list.append(match_point)
                            clustered = True
                            break

                    if not clustered:
                        match_counts[match_point].append(match_point)

        time.sleep(1.0 / iterations_per_second)

    if len(match_counts) > 0:
        return True
    
    return False
