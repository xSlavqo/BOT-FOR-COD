import cv2
import numpy as np
from mss import mss

# Wczytaj wzorzec w kolorze
template = cv2.imread('test3.png')
h, w, _ = template.shape  # Pobierz wymiary wzorca

# Zdefiniuj obszar do przechwycenia (cały ekran)
monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

with mss() as sct:
    while True:
        # Przechwyć zrzut ekranu
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)

        # Upewnij się, że obraz zrzutu ekranu ma trzy kanały (kolorowe)
        if img.shape[2] == 4:  # Jeśli zrzut ekranu jest z kanałem alfa (RGBA)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Konwertuj na BGR

        # Dopasowanie wzorca
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # Próg dopasowania
        threshold = 0.8
        if max_val >= threshold:
            top_left = max_loc
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            print(f'Koordynaty dopasowania: ({center_x}, {center_y})')

        # Wyjdź z pętli na klawisz 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
 