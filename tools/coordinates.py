import cv2
from PIL import ImageGrab
import numpy as np

points = []

def select_point(event, x, y, flags, param):
    global points, img

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        points.append((x, y))
        cv2.imshow('image', img)

def capture_screenshot_and_define_points():
    global img
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    img = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', select_point)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return points

if __name__ == "__main__":
    selected_points = capture_screenshot_and_define_points()
    print(f'Zaznaczone punkty: {selected_points}')
