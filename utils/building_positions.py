# buildings_positions.py

import cv2, numpy as np, os, json
from PIL import ImageGrab

def buildings_positions():
    main_project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    filename = os.path.join(main_project_path, "config.json")
    
    buildings = ["center", "buildings", "labo", "vest", "arch", "inf", "cav", "cele"]
    points, building_index, scale_factor = [], 0, 0.75

    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    img_original = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img_original, (0, 0), fx=scale_factor, fy=scale_factor)
    
    def select_point(event, x, y, flags, param):
        nonlocal building_index
        if event == cv2.EVENT_LBUTTONDOWN:
            original_x, original_y = int(x / scale_factor), int(y / scale_factor)
            points.append((original_x, original_y))
            cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
            print(f"Zaznaczono punkt dla {buildings[building_index]}: ({original_x}, {original_y})")
            building_index += 1
            if building_index < len(buildings):
                cv2.setWindowTitle('image', f"Zaznacz teraz: {buildings[building_index]}")
            else:
                cv2.setWindowTitle('image', "Zaznaczanie zakończone. Możesz zamknąć okno.")
                cv2.imshow('image', img)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
        cv2.imshow('image', img)
    
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', select_point)
    cv2.setWindowTitle('image', f"Zaznacz teraz: {buildings[building_index]}")
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    new_data = {f"{buildings[i]}": {"X": point[0], "Y": point[1]} for i, point in enumerate(points)}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    else:
        existing_data = {}
    
    combined_data = {**new_data, **existing_data}
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(combined_data, file, indent=4, ensure_ascii=False)
    
    print(f"Zaznaczone punkty zostały zapisane do {filename}.")
