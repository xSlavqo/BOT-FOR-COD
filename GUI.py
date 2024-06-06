import tkinter as tk
from tkinter import ttk
from threading import Thread, Event
import time
import sys
import keyboard
from screeninfo import get_monitors
from queue import Queue, Empty
from tools.functions import load_settings, load_config
from widgets import create_widgets
from execute_tasks import execute_tasks
from func_timeout import FunctionTimedOut
from tasks.cod import restart
import json

def open_window_on_specific_monitor(root, width, height, monitor_index):
    monitors = get_monitors()
    if monitor_index < len(monitors):
        monitor = monitors[monitor_index]
        x = monitor.x + (monitor.width - width) // 2
        y = monitor.y + (monitor.height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")

class RedirectedStdout:
    def __init__(self, widget, queue):
        self.widget = widget
        self.queue = queue

    def write(self, txt):
        self.queue.put(txt)

    def flush(self):
        pass

def start_loop():
    def loop(stop_event, queue):
        first_run = True
        if first_run:
            delay_time = load_config().get('delay_time')
            while delay_time > 0 and not stop_event.is_set():
                queue.put(f"Uruchomienie bota za {delay_time} sekund\n")
                time.sleep(1)
                delay_time -= 1
            first_run = False
        while not stop_event.is_set():
            try:
                execute_tasks()
                interloop_time = load_config().get('interloop_time')
                while interloop_time > 0 and not stop_event.is_set():
                    queue.put(f"uruchomienie pętli za {interloop_time} sekund\n")
                    time.sleep(1)
                    interloop_time -= 1
            except FunctionTimedOut as e:
                queue.put(f"Error: {e}\n")
                restart()
                reboot_time = load_config().get('reboot_time')
                while reboot_time > 0 and not stop_event.is_set():
                    queue.put(f"Uruchomienie po błędzie za {reboot_time} sekund\n")
                    time.sleep(1)
                    reboot_time -= 1
                continue
        queue.put("BOT zatrzymany!\n")

    global loop_thread, stop_event, queue
    stop_event = Event()
    queue = Queue()
    loop_thread = Thread(target=loop, args=(stop_event, queue))
    loop_thread.start()
    root.after(100, process_queue)

def process_queue():
    try:
        while True:
            msg = queue.get_nowait()
            terminal_text.config(state=tk.NORMAL)
            terminal_text.insert(tk.END, msg)
            terminal_text.config(state=tk.DISABLED)
            terminal_text.see(tk.END)
    except Empty:
        pass
    root.after(100, process_queue)

def stop_loop():
    stop_event.set()
    if loop_thread.is_alive():
        loop_thread.join()

root = tk.Tk()
root.title("BOT FOR COD")
window_width = 800
window_height = 800
open_window_on_specific_monitor(root, window_width, window_height, 0)

frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

settings = load_settings()
widgets = create_widgets(frame, settings)

start_button = ttk.Button(frame, text="Uruchom bota", command=start_loop)
start_button.place(x=480, y=500)

stop_button = ttk.Button(frame, text="Zatrzymaj Bota", command=stop_loop)
stop_button.place(x=480, y=540)

keyboard.add_hotkey('ctrl+z', stop_loop)

inner_frame = ttk.Frame(root, height=200)
inner_frame.pack_propagate(False)
inner_frame.pack(padx=10, pady=10, fill=tk.BOTH)
terminal_frame = ttk.LabelFrame(inner_frame, text="Terminal", padding=(5, 5))
terminal_frame.pack(fill=tk.BOTH, expand=True)

terminal_text = tk.Text(terminal_frame, wrap=tk.WORD, state=tk.DISABLED, height=10)
terminal_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
sys.stdout = RedirectedStdout(terminal_text, Queue())

def on_closing():
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
            var = widgets.vars.get(key)
            if var is not None:
                settings[key] = "true" if isinstance(var, tk.BooleanVar) and var.get() else str(var.get())

    with open(config_file, 'w', encoding='utf-8') as f:
        for key, value in settings.items():
            f.write(f"{key}={value}\n")

    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
