import sys
import tkinter as tk
from threading import Event, Thread
from tkinter import ttk
import keyboard
import time
from tools.functions import load_config, load_settings
from tools.buildings_config import buildings_config
from execute_tasks import execute_tasks
from widgets import create_widgets
from GUI_utils import init_buildings, VariableManager, StdoutRedirector, center_window_on_monitor, QueueManager

class BotGUI:
    def __init__(self):
        print("Rozpoczęcie inicjalizacji BotGUI...")

        # Inicjalizacja QueueManager i VariableManager
        self.queue_manager = QueueManager()
        self.queue_manager.create_queue('global')
        self.queue_manager.create_queue('variable')

        self.variable_manager = VariableManager(self.queue_manager.get_queue('variable'))
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
        sys.stdout = StdoutRedirector(self.terminal_text, self.queue_manager.get_queue('global'))

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
        init_buildings(self.variable_manager, self.queue_manager.get_queue('variable'))

    def start_loop(self):
        delay_time = load_config().get('delay_time', 5)

        def delayed_start(delay):
            while delay > 0 and not self.stop_event.is_set():
                self.queue_manager.put('global', f"Uruchomienie bota za {delay} sekund\n")
                time.sleep(1)
                delay -= 1

            if not self.stop_event.is_set():
                self.loop_thread = Thread(target=self.loop)
                self.loop_thread.start()

        self.stop_event.clear()
        self.loop_thread = Thread(target=delayed_start, args=(delay_time,))
        self.loop_thread.start()

    def loop(self):
        while not self.stop_event.is_set():
            execute_tasks(self.queue_manager.get_queue('global'), self.variable_manager, self.queue_manager.get_queue('variable'), self.stop_event)
            interloop_time = load_config().get('interloop_time', 0)
            while interloop_time > 0 and not self.stop_event.is_set():
                self.queue_manager.put('global', f"Uruchomienie pętli za {interloop_time} sekund\n")
                time.sleep(1)
                interloop_time -= 1

    def process_queue(self):
        self.queue_manager.process_global_queue(self.terminal_text)
        self.root.after(100, self.process_queue)

    def stop_loop(self):
        self.stop_event.set()
        self.queue_manager.put('global', "BOT zatrzymany!\n")
        if self.loop_thread is not None and self.loop_thread.is_alive():
            self.loop_thread.join()

    def execute_action1(self):
        buildings_config()

    def on_closing(self):
        self.stop_loop()
        self.root.destroy()

if __name__ == "__main__":
    app = BotGUI()
