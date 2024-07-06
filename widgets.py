import os
import tkinter as tk
from tkinter import ttk
import json

class WidgetGroup:
    def __init__(self, frame, settings, group_config, parent):
        self.frame = frame
        self.settings = settings
        self.vars = {}
        self.parent = parent
        self.create_widgets(group_config)


    def create_widgets(self, group_config):
        for group_name, items in group_config.items():
            for item in items:
                if item['type'] == 'Checkbutton':
                    var = initialize_variable(self.settings, item['key'], tk.BooleanVar)
                    widget = tk.Checkbutton(self.frame, text=item['text'], variable=var)
                    var.trace_add("write", lambda *args, key=item['key'], var=var: save_value(key, var))
                    widget.place(x=item['x'], y=item['y'])
                    self.vars[item['key']] = (widget, var)
                elif item['type'] == 'Entry':
                    var = initialize_variable(self.settings, item['key'], tk.StringVar)
                    label = ttk.Label(self.frame, text=item['text'])
                    label.place(x=0, y=0)
                    self.frame.update_idletasks()
                    label_width = label.winfo_width()
                    label.place_forget()

                    label_x = item.get('label_x', item['x'])
                    label_y = item.get('label_y', item['y'])
                    
                    entry_width = item.get('width', 4)
                    entry_x = label_x + label_width + 5
                    entry_y = label_y

                    label.place(x=label_x, y=label_y)
                    widget = ttk.Entry(self.frame, textvariable=var, width=entry_width)
                    var.trace_add("write", lambda *args, key=item['key'], var=var: save_value(key, var))
                    widget.place(x=entry_x, y=entry_y)
                    self.vars[item['key']] = (widget, var)
                elif item['type'] == 'Button':
                    command = getattr(self.parent, item['command'], None)
                    widget = ttk.Button(self.frame, text=item['text'], command=command)
                    widget.place(x=item['x'], y=item['y'])
                    self.vars[item['key']] = widget

        self.update_resource_buttons()
        self.vars['rss_map'][1].trace_add('write', self.update_resource_buttons)

    def update_resource_buttons(self, *args):
        rss_map_value = self.vars['rss_map'][1].get()
        for key in ['gold', 'wood', 'stone', 'mana']:
            widget, var = self.vars[key]
            if rss_map_value:
                widget.config(state='normal')
            else:
                widget.config(state='disabled')
                var.set(False)

def create_widgets(frame, settings, parent):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, 'widgets.json')

    with open(abs_file_path, 'r', encoding='utf-8') as f:
        widget_config = json.load(f)

    widgets = WidgetGroup(frame, settings, widget_config, parent)
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
