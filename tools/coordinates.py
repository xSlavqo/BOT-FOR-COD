import cv2
import numpy as np
import pyautogui

def match_template():
    # Zrób zrzut ekranu
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Wczytaj wzorzec z kanałem alfa
    template = cv2.imread('buduj.png', cv2.IMREAD_UNCHANGED)
    
    # Rozdzielenie kanałów RGB i Alfa
    template_rgb = template[:, :, :3]
    alpha_channel = template[:, :, 3]
    
    # Utworzenie maski na podstawie kanału alfa
    mask = alpha_channel > 0
    
    # Zapisanie maski do pliku (czarno-biały obraz)
    cv2.imwrite('mask.png', (mask * 255).astype(np.uint8))
    
    # Dopasowanie za pomocą maski, która ignoruje przezroczyste części wzorca
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    
    results = []
    
    for method in methods:
        method_eval = eval(method)
        result = cv2.matchTemplate(screenshot, template_rgb, method_eval, mask=mask.astype(np.uint8))
        
        if method in ['cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']:
            min_val, _, min_loc, _ = cv2.minMaxLoc(result)
            center_loc = (min_loc[0] + template_rgb.shape[1] // 2, min_loc[1] + template_rgb.shape[0] // 2)
            results.append((min_val, method, center_loc))
        else:
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            center_loc = (max_loc[0] + template_rgb.shape[1] // 2, max_loc[1] + template_rgb.shape[0] // 2)
            results.append((max_val, method, center_loc))
    
    # Sortowanie wyników
    results.sort(reverse=True, key=lambda x: x[0] if x[1] not in ['cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'] else -x[0])
    
    # Wyniki
    print(f'Najlepsza metoda: {results[0][1]} z wynikiem: {results[0][0]}, środek lokalizacji: {results[0][2]}')
    print(f'Drugie miejsce: {results[1][1]} z wynikiem: {results[1][0]}, środek lokalizacji: {results[1][2]}')
    print(f'Trzecie miejsce: {results[2][1]} z wynikiem: {results[2][0]}, środek lokalizacji: {results[2][2]}')

match_template()
