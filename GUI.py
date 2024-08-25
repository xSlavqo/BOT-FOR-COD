import json
import sys
import tkinter as tk
import threading
from queue import Empty, Queue
from screeninfo import get_monitors
from threading import Event, Thread
from tkinter import ttk
import keyboard
import time
from tools.functions import load_config, load_settings
from execute_tasks import execute_tasks
from widgets import create_widgets

from tools.buildings_config import buildings_config

# Klasa do przekierowywania stdout do widżetu tekstowego
class TextRedirector:
    def __init__(self, widget, queue):
        self.widget = widget
        self.queue = queue

    def write(self, txt):
        self.queue.put(txt)

    def flush(self):
        pass

class VariableManager:
    def __init__(self, queue):
        self.variables = {}
        self.queue = queue

    def process_queue(self):
        while True:
            data = self.queue.get()

            # Jeśli data jest tupli (nazwa, wartość), przechowujemy wartość
            if isinstance(data, tuple) and len(data) == 2:
                name, value = data
                self.variables[name] = value
            elif data is None:  # Sygnał do zakończenia
                break

    def start(self):
        threading.Thread(target=self.process_queue, daemon=True).start()

    def save_variables_to_file(self, file_name="variables.txt", interval=10):
        while True:
            with open(file_name, "a") as file:  # Otwieramy plik w trybie dodawania
                file.write(f"\nZapisywanie zmiennych o {time.ctime()}:\n")  # Dodaj timestamp
                for key, value in self.variables.items():
                    file.write(f"{key}: {value}\n")
            time.sleep(interval)  # Odczekaj określoną liczbę sekund przed kolejnym zapisem

    def start_saving_to_file(self, file_name="variables.txt", interval=10):
        threading.Thread(target=self.save_variables_to_file, args=(file_name, interval), daemon=True).start()


class BotGUI:
    def __init__(self):
        # Inicjalizacja głównego okna
        self.root = tk.Tk()
        self.root.title("BOT FOR COD")
        self.window_width = 1500
        self.window_height = 800
        self.open_window_on_specific_monitor(0)

        # Tworzenie głównego kontenera i widżetów
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)
        self.settings = load_settings()
        self.widgets = create_widgets(self.frame, self.settings, self)
        self.inner_frame = ttk.Frame(self.root, height=200)
        self.inner_frame.pack_propagate(False)
        self.inner_frame.pack(padx=10, pady=10, fill=tk.BOTH)
        self.terminal_frame = ttk.LabelFrame(self.inner_frame, text="Terminal", padding=(5, 5))
        self.terminal_frame.pack(fill=tk.BOTH, expand=True)
        self.terminal_text = tk.Text(self.terminal_frame, wrap=tk.WORD, state=tk.DISABLED, height=10)
        self.terminal_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Inicjalizacja kolejki i przekierowanie stdout
        self.global_queue = Queue()
        sys.stdout = TextRedirector(self.terminal_text, self.global_queue)

        # Inicjalizacja dodatkowej kolejki dla VariableManager jako atrybut instancji
        self.variable_queue = Queue()
        self.variable_manager = VariableManager(self.variable_queue)
        self.variable_manager.start()
        self.variable_manager.start_saving_to_file("variables.txt", 5)  # Zapisuj co 5 sekund

        # Konfiguracja obsługi zdarzeń
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.after(100, self.process_queue)
        self.stop_event = Event()
        self.loop_thread = None
        keyboard.add_hotkey('ctrl+z', self.stop_loop)

        # Uruchomienie pętli głównej, jeśli autostart jest włączony
        if load_config().get('autostart'):
            self.start_loop()
        self.root.mainloop()
   
    # Funkcja pomocnicza do otwierania okna na określonym monitorze
    def open_window_on_specific_monitor(self, monitor_index):
        monitors = get_monitors()
        if monitor_index < len(monitors):
            monitor = monitors[monitor_index]
            x = monitor.x + (monitor.width - self.window_width) // 2
            y = monitor.y + (monitor.height - self.window_height) // 2
            self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    # Główna pętla programu
    def loop(self):
        while not self.stop_event.is_set():
            # Poprawne przekazanie argumentów do execute_tasks    
            execute_tasks(self.global_queue, self.variable_manager, self.variable_queue, self.stop_event)
            interloop_time = load_config().get('interloop_time', 0)
            while interloop_time > 0 and not self.stop_event.is_set():
                self.global_queue.put(f"Uruchomienie pętli za {interloop_time} sekund\n")
                time.sleep(1)
                interloop_time -= 1
        self.global_queue.put("BOT zatrzymany!\n")


    # Funkcja do uruchomienia pętli głównej z opóźnieniem
    def start_loop(self):
        delay_time = load_config().get('delay_time', 0)
        def delayed_start(delay):
            while delay > 0 and not self.stop_event.is_set():
                self.global_queue.put(f"Uruchomienie bota za {delay} sekund\n")
                time.sleep(1)
                delay -= 1
            
            if not self.stop_event.is_set():
                self.loop_thread = Thread(target=self.loop)
                self.loop_thread.start()

        self.stop_event.clear()
        self.loop_thread = Thread(target=delayed_start, args=(delay_time,))
        self.loop_thread.start()

    # Funkcja do obsługi kolejki komunikatów
    def process_queue(self):
        try:
            while True:
                msg = self.global_queue.get_nowait()
                self.terminal_text.config(state=tk.NORMAL)
                self.terminal_text.insert(tk.END, msg)
                self.terminal_text.config(state=tk.DISABLED)
                self.terminal_text.see(tk.END)
        except Empty:
            pass
        self.root.after(100, self.process_queue)

    # Funkcja do zatrzymania pętli głównej
    def stop_loop(self):
        self.stop_event.set()
        if self.loop_thread is not None and self.loop_thread.is_alive():
            self.loop_thread.join()

    def execute_action1(self):
        buildings_config()

    # Funkcja do obsługi zamknięcia okna
    def on_closing(self):
        self.stop_loop()
        config_file = "config.txt"
        widgets_config_file = "widgets.json"

        try:
            with open(widgets_config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config_data = {}

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                settings = {line.split('=')[0]: line.split('=')[1].strip() for line in f}
        except (FileNotFoundError, ValueError):
            settings = {}

        for section, items in config_data.items():
            for item in items:
                key = item['key']
                widget_var_tuple = self.widgets.vars.get(key)
                if widget_var_tuple is not None and isinstance(widget_var_tuple, (tuple, list)):
                    widget, var = widget_var_tuple
                    settings[key] = "true" if isinstance(var, tk.BooleanVar) and var.get() else str(var.get())

        with open(config_file, 'w', encoding='utf-8') as f:
            for key, value in settings.items():
                f.write(f"{key}={value}\n")

        self.root.destroy()

# Główna część programu
if __name__ == "__main__":
    app = BotGUI()
