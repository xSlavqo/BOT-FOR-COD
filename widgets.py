import tkinter as tk
from tkinter import ttk

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
                    if command:
                        widget = ttk.Button(self.frame, text=item['text'], command=command)
                    else:
                        widget = ttk.Button(self.frame, text=item['text'])
                    widget.place(x=item['x'], y=item['y'])
                    self.vars[item['key']] = widget

                elif item['type'] == 'Combobox':
                    var = initialize_variable(self.settings, item['key'], tk.StringVar)
                    widget = ttk.Combobox(self.frame, textvariable=var, values=item['values'], width=item.get('width', 10))
                    var.trace_add("write", lambda *args, key=item['key'], var=var: save_value(key, var))
                    widget.place(x=item['x'], y=item['y'])
                    self.vars[item['key']] = (widget, var)

        self.update_buttons('rss_map', ['gold', 'wood', 'stone', 'mana'])
        self.vars['rss_map'][1].trace_add('write', lambda *args: self.update_buttons('rss_map', ['gold', 'wood', 'stone', 'mana']))

        self.update_buttons('train_units', ['vest', 'arch', 'inf', 'cav', 'cele', 'vest_tier', 'arch_tier', 'inf_tier', 'cav_tier', 'cele_tier'])
        self.vars['train_units'][1].trace_add('write', lambda *args: self.update_buttons('train_units', ['vest', 'arch', 'inf', 'cav', "cele", 'vest_tier', 'arch_tier', 'inf_tier', 'cav_tier', 'cele_tier']))

    def update_buttons(self, key, button_keys, *args):
        button_type = self.vars[key][1].get()
        for button_key in button_keys:
            widget, var = self.vars[button_key]
            if button_type:
                widget.config(state='normal')
            else:
                widget.config(state='disabled')
                if isinstance(var, tk.BooleanVar):
                    var.set(False)
                elif isinstance(var, tk.StringVar):
                    var.set('')

    

def create_widgets(frame, settings, parent):
    widget_config = {
        "Mapa": [
            {"type": "Checkbutton", "text": "Zbieraj surowce", "key": "rss_map", "x": 50, "y": 50},
            {"type": "Checkbutton", "text": "Złoto", "key": "gold", "x": 50, "y": 80},
            {"type": "Checkbutton", "text": "Drewno", "key": "wood", "x": 50, "y": 110},
            {"type": "Checkbutton", "text": "Kamień", "key": "stone", "x": 50, "y": 140},
            {"type": "Checkbutton", "text": "Mana", "key": "mana", "x": 50, "y": 170},
            {"type": "Entry", "text": "Maksymalna ilość legionów", "key": "max_gathers", "x": 50, "y": 200}
        ],
        "Miasto": [
            {"type": "Checkbutton", "text": "Leczenie jednostek", "key": "hospital", "x": 450, "y": 50},
            {"type": "Checkbutton", "text": "Automatyczna budowa", "key": "auto_build", "x": 450, "y": 80},
            {"type": "Checkbutton", "text": "Dialogi bohaterów", "key": "dialogues", "x": 450, "y": 110},
            {"type": "Checkbutton", "text": "Szkolenie jednostek", "key": "train_units", "x": 450, "y": 200},
            {"type": "Checkbutton", "text": "Westalki", "key": "vest", "x": 450, "y": 230},
            {"type": "Combobox", "text": "", "key": "vest_tier", "values": ["T1", "T2", "T3","T4","T5"], "x": 580, "y": 230, "width": 5},
            {"type": "Checkbutton", "text": "Łucznicy", "key": "arch", "x": 450, "y": 260},
            {"type": "Combobox", "text": "", "key": "arch_tier", "values": ["T1", "T2", "T3","T4","T5"], "x": 580, "y": 260, "width": 5},
            {"type": "Checkbutton", "text": "Piechota", "key": "inf", "x": 450, "y": 290},
            {"type": "Combobox", "text": "", "key": "inf_tier", "values": ["T1", "T2", "T3","T4","T5"], "x": 580, "y": 290, "width": 5},
            {"type": "Checkbutton", "text": "Kawaleria", "key": "cav", "x": 450, "y": 320},
            {"type": "Combobox", "text": "", "key": "cav_tier", "values": ["T1", "T2", "T3","T4","T5"], "x": 580, "y": 320, "width": 5},
            {"type": "Checkbutton", "text": "Niebianie", "key": "cele", "x": 450, "y": 350},
            {"type": "Combobox", "text": "", "key": "cele_tier", "values": ["T3","T4","T5"], "x": 580, "y": 350, "width": 5}
        ],
        "Sojusz": [
            {"type": "Checkbutton", "text": "Pomoc sojuszu", "key": "ally_help", "x": 850, "y": 50},
            {"type": "Checkbutton", "text": "Odbierz prezenty sojuszu", "key": "ally_gifts", "x": 850, "y": 80}
        ],
        "Overall": [
            {"type": "Entry", "text": "Opóźnienie uruchomienia", "key": "delay_time", "x": 50, "y": 270},
            {"type": "Entry", "text": "Czas między pętlami", "key": "interloop_time", "x": 50, "y": 300},
            {"type": "Entry", "text": "Czas restartu po błędzie", "key": "reboot_time", "x": 50, "y": 330},
            {"type": "Checkbutton", "text": "Autostart", "key": "autostart", "x": 50, "y": 360},
            {"type": "Entry", "text": "Opóźnienie autostartu", "key": "autostart_delay", "x": 50, "y": 390},
            {"type": "Button", "text": "Uruchom bota", "key": "start_button", "x": 1250, "y": 450, "command": "start_loop"},
            {"type": "Button", "text": "Zatrzymaj Bota", "key": "stop_button", "x": 1250, "y": 480, "command": "stop_loop"},
            {"type": "Button", "text": "Konfiguracja położenia budynków", "key": "execute_action1", "x": 1250, "y": 510, "command": "execute_action1"}
        ]
    }

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
