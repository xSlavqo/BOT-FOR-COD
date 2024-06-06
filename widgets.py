import os
import tkinter as tk
from tkinter import ttk
import json
import tkinter as tk

class WidgetGroup:
    def __init__(self, frame, settings, group_config):
        self.frame = frame
        self.settings = settings
        self.vars = {}
        self.create_widgets(group_config)

    def create_widgets(self, group_config):
        for group_name, items in group_config.items():
            for item in items:
                if item['type'] == 'Checkbutton':
                    var = initialize_variable(self.settings, item['key'], tk.BooleanVar)
                    widget = tk.Checkbutton(self.frame, text=item['text'], variable=var)
                    var.trace_add("write", lambda *args, key=item['key'], var=var: save_value(key, var))
                    widget.place(x=item['x'], y=item['y'])
                elif item['type'] == 'Entry':
                    var = initialize_variable(self.settings, item['key'], tk.StringVar)
                    # Utwórz etykietę
                    label = ttk.Label(self.frame, text=item['text'])
                    label.place(x=0, y=0)  # Tymczasowe umieszczenie
                    self.frame.update_idletasks()  # Aktualizacja ramki, aby uzyskać rzeczywiste wymiary etykiety
                    label_width = label.winfo_width()
                    label_height = label.winfo_height()
                    label.place_forget()  # Usunięcie tymczasowego umieszczenia

                    # Ustal pozycje etykiety
                    label_x = item.get('label_x', item['x'])
                    label_y = item.get('label_y', item['y'])
                    
                    # Ustal szerokość i pozycję pola wejściowego
                    entry_width = item.get('width', 4)  # Domyślna szerokość to 20 znaków
                    entry_x = label_x + label_width + 5  # Dodaj odstęp 5 pikseli między etykietą a polem wejściowym
                    entry_y = label_y

                    # Umieść etykietę i pole wejściowe na ramce
                    label.place(x=label_x, y=label_y)
                    widget = ttk.Entry(self.frame, textvariable=var, width=entry_width)
                    var.trace_add("write", lambda *args, key=item['key'], var=var: save_value(key, var))
                    widget.place(x=entry_x, y=entry_y)
                self.vars[item['key']] = var

def create_widgets(frame, settings):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, 'widgets.json')
    
    with open(abs_file_path, 'r', encoding='utf-8') as f:
        widget_config = json.load(f)

    widgets = WidgetGroup(frame, settings, widget_config)
    return widgets

def save_value(key, var):
    try:
        with open("config.txt", 'r', encoding='utf-8') as f:
            settings = {}
            for line in f:
                k, value = line.strip().split('=')
                settings[k] = value
    except (FileNotFoundError, ValueError):
        settings = {}

    if isinstance(var, tk.BooleanVar):
        settings[key] = "true" if var.get() else "false"
    else:
        settings[key] = var.get()

        # Zapisywanie zaktualizowanych wartości do pliku config.txt
    with open("config.txt", 'w', encoding='utf-8') as f:
        for k, v in settings.items():
            f.write(f"{k}={v}\n")

def initialize_variable(settings, key, var_type):
    value = settings.get(key, "")
    variable = var_type()
    if var_type == tk.BooleanVar:
        variable.set(value.lower() == 'true')
    else:
        variable.set(value)
    return variable