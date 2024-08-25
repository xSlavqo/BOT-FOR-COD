import threading
import queue

# Kolejka do komunikacji między wątkami
variable_queue = queue.Queue()

# Słownik do przechowywania zmiennych
variable_storage = {}

# Funkcja B: Dodaje zmienne do kolejki
def add_variable(name, value):
    variable_queue.put((name, value))

# Funkcja A: Monitoruje kolejkę i aktualizuje słownik
def variable_manager():
    while True:
        # Sprawdzanie, czy w kolejce są nowe zmienne
        while not variable_queue.empty():
            name, value = variable_queue.get()
            variable_storage[name] = value

# Funkcja do zbierania danych od użytkownika
def user_input_listener():
    while True:
        command = input("Podaj 'ok', aby wyświetlić zmienne, 'exit' by zakończyć, lub wprowadź zmienną: ")
        if command == "ok":
            print("Aktualne wartości zmiennych:")
            for name, value in variable_storage.items():
                print(f"{name}: {value}")
        elif command == "exit":
            print("Kończę program.")
            break
        else:
            # Zakładamy, że użytkownik chce wprowadzić zmienną
            name, value = command.split("=")
            add_variable(name.strip(), value.strip())

# Uruchomienie funkcji A w osobnym wątku
manager_thread = threading.Thread(target=variable_manager, daemon=True)
manager_thread.start()

# Uruchomienie funkcji do zbierania danych od użytkownika w głównym wątku
user_input_listener()
