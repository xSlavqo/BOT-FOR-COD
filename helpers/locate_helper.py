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
    match_values = correlation[correlation >= threshold]
    return matches, match_values, max_val, correlation  # Zwracamy również 'correlation'

def filter_overlapping_matches(matches, template_shape):
    filtered_matches = []
    for match in matches:
        top_left = match
        bottom_right = (top_left[0] + template_shape[1], top_left[1] + template_shape[0])

        if not any(
            (top_left[0] < m[1] and bottom_right[0] > m[0] and top_left[1] < m[3] and bottom_right[1] > m[2])
            for m in filtered_matches
        ):
            filtered_matches.append((top_left[0], bottom_right[0], top_left[1], bottom_right[1]))

    return [(m[0], m[2]) for m in filtered_matches]

def locate_and_draw_matches(img, template, threshold):
    matches, match_values, max_val, correlation = is_image_match(img, template, threshold)
    filtered_matches = filter_overlapping_matches(matches, template.shape)

    print("Regiony wystąpień dopasowań:")
    max_similarity = match_values.max() if len(match_values) > 0 else max_val
    min_similarity = match_values.min() if len(match_values) > 0 else 0
    total_matches = len(filtered_matches)

    for top_left in filtered_matches:
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        print(f"Top-left: {top_left}, Bottom-right: {bottom_right}")
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 3)

    max_matches = [(x, y) for (x, y) in filtered_matches if correlation[y, x] == max_similarity]

    print("\nMaksymalne dopasowania (w progu):")
    for top_left in max_matches:
        print(f"Top-left: {top_left}")

    return img, max_similarity, min_similarity, total_matches

def locate_helper(template_path, threshold):
    cod_window = gw.getWindowsWithTitle("Call of Dragons")
    if not cod_window:
        print("Nie znaleziono okna: Call of Dragons")
        return

    cod_window[0].activate()

    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    
    with mss.mss() as sct:
        monitor = {
            "top": cod_window[0].top,
            "left": cod_window[0].left,
            "width": cod_window[0].width,
            "height": cod_window[0].height
        }
        while True:
            screen_shot = sct.grab(monitor)
            img = np.array(screen_shot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            img_with_match, max_similarity, min_similarity, total_matches = locate_and_draw_matches(img, template, threshold)
            print(f"Maksymalne podobieństwo: {max_similarity:.10f} | Minimalne trafienie: {min_similarity:.10f} | Łączna liczba dopasowań: {total_matches}")

            img_resized = cv2.resize(img_with_match, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_AREA)
            cv2.imshow("Call of Dragons", img_resized)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    locate_helper("r.png", 0.9999)
