import cv2
import numpy as np
import mss

def is_image_match(img, template, threshold):
    base = template[:, :, :3]
    alpha_mask = cv2.merge([template[:, :, 3]] * 3)
    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha_mask)
    max_val = correlation.max()
    matches = list(zip(*np.where(correlation >= threshold)[::-1]))
    return matches, max_val

def locate_and_evaluate(template_path, threshold):
    # Wczytanie obrazu szablonu z kanałem alfa
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    best_match_value = 0
    best_match_location = None

    with mss.mss() as sct:
        monitor = sct.monitors[2] if len(sct.monitors) > 2 else sct.monitors[1]
        screen_shot = sct.grab(monitor)
        img = np.array(screen_shot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        matches, max_val = is_image_match(img, template, threshold)

        if max_val > best_match_value:
            best_match_value = max_val
            best_match_location = matches[0] if matches else None

        if best_match_location:
            # Rysowanie prostokąta wokół najlepszego dopasowania
            top_left = best_match_location
            bottom_right = (
                top_left[0] + template.shape[1],
                top_left[1] + template.shape[0],
            )
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

            # Wyświetlenie obrazu z zaznaczonym fragmentem
            cv2.imshow("Best Match", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    return best_match_value * 100, best_match_location

if __name__ == "__main__":
    match_percentage, match_location = locate_and_evaluate("png/build/build_new.png", 0.999)
    print(f"Dopasowanie: {match_percentage:.2f}%")
    if match_location:
        print(f"Najlepszy fragment: {match_location}")
