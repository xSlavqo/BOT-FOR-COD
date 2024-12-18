import pygetwindow as gw
import mss


def find_call_of_dragons_monitor():
    try:
        # Znajdź okno Call of Dragons
        window = gw.getWindowsWithTitle('Call of Dragons')[0]  # Pobierz pierwsze pasujące okno
        window_x, window_y = window.left, window.top  # Pozycja lewego górnego rogu okna

        with mss.mss() as sct:
            for index, monitor in enumerate(sct.monitors[1:], start=1):  # Pomijamy sct.monitors[0], bo to cały obszar
                mon_left = monitor['left']
                mon_top = monitor['top']
                mon_width = monitor['width']
                mon_height = monitor['height']

                if (mon_left <= window_x < mon_left + mon_width) and (mon_top <= window_y < mon_top + mon_height):
                    return index  # Zwracamy numer monitora, na którym znajduje się okno Call of Dragons

        raise Exception("Nie znaleziono monitora z Call of Dragons")
    except IndexError:
        raise Exception("Nie znaleziono okna Call of Dragons")


if __name__ == "__main__":
    try:
        monitor_index = find_call_of_dragons_monitor()
        print(f"Call of Dragons jest na monitorze o indeksie: {monitor_index}")
    except Exception as e:
        print(e)
