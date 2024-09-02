import json
import sys
import tkinter as tk
import threading
from queue import Empty
from threading import Event, Thread
from tkinter import ttk
import keyboard
import time
from tools.functions import load_config, load_settings
from execute_tasks import execute_tasks
from widgets import create_widgets
from GUI_utils import building_main, VariableManager, StdoutRedirector, center_window_on_monitor, queue_manager, QueueManager
from tools.buildings_config import buildings_config
import threading


class BotGUI:
    def __init__(self):
        print("Rozpoczęcie inicjalizacji BotGUI...")
        
        # Inicjalizacja QueueManager bezpośrednio w tym pliku
        global queue_manager
        queue_manager = QueueManager()
        queue_manager.create_queue('global')
        queue_manager.create_queue('variable')
        print("QueueManager zainicjalizowany globalnie:", queue_manager)

        # Sprawdzamy, czy queue_manager został poprawnie zainicjalizowany
        if not queue_manager:
            raise RuntimeError("QueueManager nie został poprawnie zainicjalizowany!")

        # Inicjalizacja VariableManager
        self.variable_manager = VariableManager(queue_manager.get_queue('variable'))
        self.variable_manager.start()

        # Dodajemy inicjalizację budynków
        self.init_buildings()

        # Inicjalizacja głównego okna
        self.root = tk.Tk()
        self.root.title("BOT FOR COD")
        self.window_width = 1500
        self.window_height = 800

        # Wycentrowanie okna na wybranym monitorze
        center_window_on_monitor(self.root, 0, self.window_width, self.window_height)

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

        # Przekierowanie stdout do global_queue
        sys.stdout = StdoutRedirector(self.terminal_text, queue_manager.get_queue('global'))

        # Konfiguracja obsługi zdarzeń
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.after(100, self.process_queue)
        self.stop_event = Event()
        self.loop_thread = None
        keyboard.add_hotkey('ctrl+z', self.stop_loop)

        # Uruchomienie pętli głównej, jeśli autostart jest włączony
        if load_config().get('autostart'):
            self.start_loop()

        # Uruchomienie głównej pętli Tkintera
        self.root.mainloop()

    def init_buildings(self):
        building_main(self.variable_manager, queue_manager.get_queue('variable'))


    def start_loop(self):
        delay_time = load_config().get('delay_time', 0)

        def delayed_start(delay):
            while delay > 0 and not self.stop_event.is_set():
                queue_manager.put('global', f"Uruchomienie bota za {delay} sekund\n")
                time.sleep(1)
                delay -= 1

            if not self.stop_event.is_set():
                self.loop_thread = Thread(target=self.loop)
                self.loop_thread.start()

        self.stop_event.clear()
        self.loop_thread = Thread(target=delayed_start, args=(delay_time,))
        self.loop_thread.start()

    # Główna pętla programu
    def loop(self):
        while not self.stop_event.is_set():
            execute_tasks(queue_manager.get_queue('global'), self.variable_manager, queue_manager.get_queue('variable'), self.stop_event)
            interloop_time = load_config().get('interloop_time', 0)
            while interloop_time > 0 and not self.stop_event.is_set():
                queue_manager.put('global', f"Uruchomienie pętli za {interloop_time} sekund\n")
                time.sleep(1)
                interloop_time -= 1

    # Funkcja do obsługi kolejki komunikatów
    def process_queue(self):
        """Przetwarzanie global_queue i aktualizacja terminala."""
        queue_manager.process_global_queue(self.terminal_text)
        self.root.after(100, self.process_queue)

    # Funkcja do zatrzymania pętli głównej
    def stop_loop(self):
        self.stop_event.set()
        queue_manager.put('global', "BOT zatrzymany!\n")
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
