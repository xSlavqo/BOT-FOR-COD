import cv2
from PIL import ImageGrab
import numpy as np
import time

regions = []
drawing = False
ix, iy = -1, -1

def select_region(event, x, y, flags, param):
    global ix, iy, drawing, regions, img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img2 = img.copy()
            cv2.rectangle(img2, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        regions.append((ix, iy, x - ix, y - iy))
        cv2.imshow('image', img)

def capture_screenshot_and_define_regions():
    global img
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    img = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', select_region)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return regions

if __name__ == "__main__":

    time.sleep(2)
    selected_regions = capture_screenshot_and_define_regions()
    print(f'Zaznaczone regiony: {selected_regions}')