import tkinter as tk

CONFIG_FILE = "config.txt"

def load_settings():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            settings = {}
            for line in f:
                key, value = line.strip().split('=')
                settings[key] = value
            return settings
    except (FileNotFoundError, ValueError):
        return {}

def load_config():
    config_values = {}
    with open(CONFIG_FILE, 'r', encoding='utf-8') as config_file:
        for line in config_file:
            key, value = line.strip().split('=')
            if value.lower() == 'true':
                config_values[key] = True
            elif value.lower() == 'false':
                config_values[key] = False
            else:
                try:
                    config_values[key] = int(value)
                except ValueError:
                    try:
                        config_values[key] = float(value)
                    except ValueError:
                        config_values[key] = value
    return config_values
