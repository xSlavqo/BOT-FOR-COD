import threading
import tkinter as tk
from queue import Queue, Empty
from screeninfo import get_monitors
from building_menager.building import Building

queue_manager = None

class StdoutRedirector:
    def __init__(self, widget, queue):
        self.widget = widget
        self.queue = queue

    def write(self, txt):
        self.queue.put(txt)

    def flush(self):
        pass

def center_window_on_monitor(window, monitor_index=0, width=1500, height=800):
    monitors = get_monitors()
    if monitor_index < len(monitors):
        monitor = monitors[monitor_index]
        x = monitor.x + (monitor.width - width) // 2
        y = monitor.y + (monitor.height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

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

class QueueManager:
    def __init__(self):
        self.queues = {}

    def create_queue(self, name):
        self.queues[name] = Queue()
        print(f"Kolejka '{name}' utworzona!")

    def get_queue(self, name):
        return self.queues.get(name)

    def put(self, name, data):
        if name in self.queues:
            self.queues[name].put(data)

    def get(self, name, timeout=1):
        if name in self.queues:
            try:
                return self.queues[name].get(timeout=timeout)
            except Empty:
                return None

    def process_global_queue(self, terminal_widget):
        """Przetwarzanie kolejki 'global' i aktualizacja terminala Tkinter."""
        try:
            while True:
                msg = self.queues['global'].get_nowait()
                terminal_widget.config(state=tk.NORMAL)
                terminal_widget.insert(tk.END, msg)
                terminal_widget.config(state=tk.DISABLED)
                terminal_widget.see(tk.END)
        except Empty:
            pass

def building_main(variable_manager, variable_queue):
    building_names = ["center", "buildings", "labo", "vest", "arch", "inf", "cav", "cele"]
    buildings = {name: Building(name=name) for name in building_names}

    variable_queue.put(('buildings', buildings))
    print("Budynki utworzone!")


