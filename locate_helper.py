# locate_helper.py
import cv2
import numpy as np
import mss
import pygetwindow as gw

def is_image_match(img, template, threshold):
    base = template[:, :, :3]
    alpha_mask = cv2.merge([template[:, :, 3]] * 3)
    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha_mask)
    max_val = correlation.max()
    matches = list(zip(*np.where(correlation >= threshold)[::-1]))
    return matches, max_val

def locate_and_draw_matches(img, template, threshold):
    matches, max_val = is_image_match(img, template, threshold)
    for top_left in matches:
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 3)
    return img, max_val

def locate_helper(template_path, threshold=0.99, window_name="Call of Dragons"):
    window = gw.getWindowsWithTitle(window_name)
    if not window:
        print(f"Nie znaleziono okna: {window_name}")
        return
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    
    with mss.mss() as sct:
        monitor = {
            "top": window[0].top,
            "left": window[0].left,
            "width": window[0].width,
            "height": window[0].height
        }
        while True:
            screen_shot = sct.grab(monitor)
            img = np.array(screen_shot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            img_with_match, max_similarity = locate_and_draw_matches(img, template, threshold)
            print(f"Maksymalne podobieństwo: {max_similarity:.4f}")

            img_resized = cv2.resize(img_with_match, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_AREA)
            cv2.imshow(window_name, img_resized)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    locate_helper("city.png", 0.99)