import cv2
from PIL import ImageGrab
import numpy as np

regions = []
drawing = False
ix, iy = -1, -1
scale = 0.75  # Skalowanie podglądu do 75%

def on_mouse(event, x, y, flags, param):
    global ix, iy, drawing, regions, img_copy

    # Przeskaluj współrzędne na podstawie skali podglądu
    x_orig, y_orig = int(x / scale), int(y / scale)

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x_orig, y_orig

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img_resized.copy()
            cv2.rectangle(img_copy, (int(ix * scale), int(iy * scale)), (x, y), (0, 255, 0), 2)
            cv2.imshow("Screenshot", img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        width, height = x_orig - ix, y_orig - iy
        regions.append((ix, iy, width, height))
        cv2.rectangle(img_resized, (int(ix * scale), int(iy * scale)), (x, y), (0, 255, 0), 2)
        cv2.imshow("Screenshot", img_resized)

def capture_screenshot_and_define_regions():
    global img, img_resized, img_copy
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    img = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    # Zmniejsz obraz do 75% tylko dla podglądu
    img_resized = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    img_copy = img_resized.copy()

    cv2.namedWindow("Screenshot")
    cv2.setMouseCallback("Screenshot", on_mouse)
    cv2.imshow("Screenshot", img_resized)

    while True:
        if cv2.waitKey(1) & 0xFF == 27:  # Naciśnij ESC, aby zakończyć wybieranie regionów
            break

    cv2.destroyAllWindows()
    return regions

if __name__ == "__main__":
    import time
    time.sleep(2)  # Przerwa przed zrobieniem zrzutu ekranu
    selected_regions = capture_screenshot_and_define_regions()
    print(f'Zaznaczone regiony: {selected_regions}')
