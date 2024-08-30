import cv2
import numpy as np
import pygetwindow as gw
from PIL import ImageGrab
import os
import time

def buildings_config(window_title="Call of Dragons"):
    # Ustawienia
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "buildings.txt")
    buildings = ["center", "buildings", "labo", "vest", "arch", "inf", "cav", "cele"]
    points = []
    building_index = 0
    scale_factor = 0.8  # Skalowanie do 80%

    # Znajdź okno o podanym tytule
    window = gw.getWindowsWithTitle(window_title)
    if not window:
        print(f"Nie znaleziono okna o tytule: {window_title}")
        return None

    window = window[0]
    window.activate()

    time.sleep(1)

    # Zrzut ekranu obszaru okna
    bbox = (window.left, window.top, window.right, window.bottom)
    screenshot = ImageGrab.grab(bbox=bbox)
    screenshot_np = np.array(screenshot)
    img_original = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    # Przeskalowanie obrazu
    img_scaled = cv2.resize(img_original, (0, 0), fx=scale_factor, fy=scale_factor)
    img = img_scaled

    # Funkcja obsługi kliknięć myszą
    def select_point(event, x, y, flags, param):
        nonlocal building_index
        if event == cv2.EVENT_LBUTTONDOWN:
            # Przeliczenie współrzędnych na skalę 100%
            original_x = int(x / scale_factor)
            original_y = int(y / scale_factor)
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

    # Wyświetlenie obrazu i oczekiwanie na kliknięcia
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', select_point)
    cv2.setWindowTitle('image', f"Zaznacz teraz: {buildings[building_index]}")
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Zapis punktów do pliku
    with open(filename, "w", encoding="utf-8") as file:
        for i, point in enumerate(points):
            file.write(f"{buildings[i]}_x = {point[0]}\n")
            file.write(f"{buildings[i]}_y = {point[1]}\n")

    print(f"Zaznaczone punkty zostały zapisane do {filename}.")



def load_building_coordinates():
    region = {}
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "buildings.txt")
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                unit = lines[i].split('_')[0]
                x = int(lines[i].split('=')[1].strip())
                y = int(lines[i+1].split('=')[1].strip())
                region[unit] = (x, y)
    except FileNotFoundError:
        print("Plik buildings.txt nie został znaleziony.")
    return region