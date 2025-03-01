# read_screen_text.py
from PIL import ImageGrab
import pytesseract
import pygetwindow as gw

def get_game_window_region(window_title="Call of Dragons"):
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        game_window = windows[0]
        if game_window.isMinimized:
            game_window.restore()
        left, top = game_window.left, game_window.top
        right, bottom = left + game_window.width, top + game_window.height
        print(f"Region okna: {left}, {top}, {right}, {bottom}")  # Debug
        return (left, top, right, bottom)
    else:
        print("Nie znaleziono okna gry Call of Dragons.")
        return None


def read_text_from_screen(region=None, lang="pol"):
    """
    Odczytuje tekst z ekranu za pomocą OCR.
    
    Parametry:
      region (tuple): (left, top, right, bottom) definiujący region ekranu.
                      Jeśli None, odczytuje z całego ekranu.
      lang (str): Język OCR (domyślnie "pol").
    
    Zwraca:
      str: Odczytany tekst.
    """
    try:
        screenshot = ImageGrab.grab(bbox=region) if region else ImageGrab.grab()
        text = pytesseract.image_to_string(screenshot, lang=lang)
        return text.strip()
    except Exception as e:
        print(f"Błąd podczas odczytywania tekstu z ekranu: {e}")
        return ""

def read_text_from_game(lang="pol"):
    """
    Odczytuje tekst z okna gry Call of Dragons.
    
    Najpierw ustala region okna, a następnie wykorzystuje OCR
    do odczytania tekstu z tego regionu.
    
    Parametry:
      lang (str): Język OCR (domyślnie "pol").
    
    Zwraca:
      str: Odczytany tekst, lub pusty string w przypadku błędu.
    """
    region = get_game_window_region()
    if region is not None:
        return read_text_from_screen(region, lang=lang)
    else:
        return ""


# Przykładowy region: (1703, 163, 206, 365) – czyli x, y, szerokość, wysokość
tekst = read_text_from_screen((1703, 163, 206, 365), lang="pol")
print("Odczytany tekst:", tekst)
