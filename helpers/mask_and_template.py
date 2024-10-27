import cv2
import numpy as np
import os
from PIL import Image
import random

def utworz_i_zastosuj_maske(directory, threshold_value=30):
    first_image = True
    mask = None
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Tworzenie maski wspólnych elementów
    for filename in image_files:
        filepath = os.path.join(directory, filename)
        image = cv2.imread(filepath)

        if first_image:
            mask = np.ones_like(image) * 255
            first_image = False
            base_image = image
        else:
            diff = cv2.absdiff(base_image, image)
            grey_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(grey_diff, threshold_value, 255, cv2.THRESH_BINARY)
            thresh_inv = cv2.bitwise_not(thresh)
            mask = cv2.bitwise_and(mask, mask, mask=thresh_inv)

    # Zapisanie tymczasowej maski
    tmp_mask_path = os.path.join(directory, 'temp_mask.png')
    cv2.imwrite(tmp_mask_path, mask)

    # Wybór losowego obrazu do nałożenia maski
    selected_image_path = os.path.join(directory, random.choice(image_files))

    # Nałożenie maski z przezroczystością na wybrany losowo obraz
    try:
        obraz = Image.open(selected_image_path).convert("RGBA")
        maska = Image.open(tmp_mask_path).convert("L")
        wynikowy_obraz = Image.new("RGBA", obraz.size)

        for x in range(obraz.width):
            for y in range(obraz.height):
                piksel_maski = maska.getpixel((x, y))
                if piksel_maski == 255:
                    wynikowy_obraz.putpixel((x, y), obraz.getpixel((x, y)))
                else:
                    wynikowy_obraz.putpixel((x, y), (0, 0, 0, 0))

        sciezka_wynikowa = os.path.join(directory, 'result.png')
        wynikowy_obraz.save(sciezka_wynikowa)
        print(f"Obraz z nałożoną maską zapisany jako: {sciezka_wynikowa}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

# Przykładowe użycie
directory = "stay"
threshold_value = 1

utworz_i_zastosuj_maske(directory, threshold_value)
