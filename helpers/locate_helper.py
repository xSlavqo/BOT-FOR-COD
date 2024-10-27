# locate_helper.py
import cv2
import numpy as np
import mss

def is_image_match(img, template, threshold):
    base = template[:, :, :3]
    alpha_mask = cv2.merge([template[:, :, 3]] * 3)
    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha_mask)
    max_val = correlation.max()  # Najlepsze dopasowanie, nawet poniżej progu
    matches = list(zip(*np.where(correlation >= threshold)[::-1]))
    match_values = correlation[correlation >= threshold]  # Wartości podobieństwa dla trafień powyżej progu
    return matches, match_values, max_val

def filter_overlapping_matches(matches, template_shape):
    filtered_matches = []
    for match in matches:
        top_left = match
        bottom_right = (top_left[0] + template_shape[1], top_left[1] + template_shape[0])

        # Sprawdzenie, czy dopasowanie nachodzi na inne zapisane wcześniej dopasowania
        if not any(
            (top_left[0] < m[1] and bottom_right[0] > m[0] and top_left[1] < m[3] and bottom_right[1] > m[2])
            for m in filtered_matches
        ):
            filtered_matches.append((top_left[0], bottom_right[0], top_left[1], bottom_right[1]))

    return filtered_matches  # Zwracamy pełne regiony dopasowań

def locate_and_draw_matches(img, template, threshold, search_regions):
    all_filtered_matches = []
    all_match_values = []
    max_similarity = 0  # Inicjalizacja maksymalnego dopasowania poza progiem

    for region in search_regions:
        # Wycięcie regionu z obrazu
        cropped_img = img[
            region["top"]:region["top"] + region["height"],
            region["left"]:region["left"] + region["width"]
        ]

        matches, match_values, max_val = is_image_match(cropped_img, template, threshold)
        filtered_matches = filter_overlapping_matches(matches, template.shape)

        # Aktualizacja wartości maksymalnego dopasowania nawet poza progiem
        max_similarity = max(max_similarity, max_val)

        # Dodajemy przesunięcie regionu do znalezionych punktów
        for match, value in zip(filtered_matches, match_values):
            adjusted_match = (match[0] + region["left"], match[1] + region["top"])
            all_filtered_matches.append(adjusted_match)
            all_match_values.append(value)
            cv2.rectangle(
                img,
                adjusted_match,
                (adjusted_match[0] + template.shape[1], adjusted_match[1] + template.shape[0]),
                (0, 255, 0), 3
            )

    # Drukowanie wartości dopasowania dla każdego znalezionego dopasowania
    if all_match_values:
        print("Wartości dopasowań dla znalezionych obiektów:")
        for idx, value in enumerate(all_match_values, start=1):
            print(f"Dopasowanie {idx}: {value:.10f}")
    else:
        print(f"Brak dopasowań powyżej progu. Najlepsze dopasowanie: {max_similarity:.10f}")

    total_matches = len(all_filtered_matches)
    return img, max_similarity, total_matches

def locate_helper(template_path, threshold, search_regions=None):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

    # Przygotowanie pełnego regionu monitora
    with mss.mss() as sct:
        monitor = sct.monitors[2]  # Ustawienie na cały pierwszy monitor

        while True:
            screen_shot = sct.grab(monitor)
            img = np.array(screen_shot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # Przeszukiwanie ograniczonych regionów
            img_with_match, max_similarity, total_matches = locate_and_draw_matches(
                img, template, threshold, search_regions
            )
            print(f"Maksymalne podobieństwo znalezione poza progiem (jeśli brak dopasowań): {max_similarity:.10f} | Łączna liczba dopasowań: {total_matches}")

            # Skala podglądu tylko do wyświetlenia
            img_resized = cv2.resize(img_with_match, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_AREA)
            cv2.imshow("Podgląd", img_resized)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    search_regions = []
    
    locate_helper("png/city.png", 0.97, search_regions=search_regions)
