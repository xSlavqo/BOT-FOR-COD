import pyautogui
import time

time.sleep(5)
# Lista koordynatów do klikania po kolei
coordinates = [
    (1006, 528),
    (1052, 627),
    (1386, 877),
    (1003, 533),
    (1005, 634),
    (1272, 661),
    (1152, 666),
    (1288, 423),
    (1162, 427),
    (1272, 424),
    (999, 517)
]

# Funkcja wykonująca kliknięcia w zadanych koordynatach
def click_coordinates(coords, interval=1):
    for coord in coords:
        pyautogui.mouseDown(coord[0], coord[1])
        time.sleep(0.1)  # Krótkie przytrzymanie przycisku
        pyautogui.mouseUp(coord[0], coord[1])
        time.sleep(interval)

# Wywołanie funkcji 309 razy
for _ in range(8):
    click_coordinates(coordinates)
