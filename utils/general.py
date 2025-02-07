# utils/general.py

import json

CONFIG_PATH = "config.json"

def read_config(file_path=CONFIG_PATH):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def write_config(key, value, file_path=CONFIG_PATH):
    try:
        config = read_config(file_path)
        config[key] = value
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Nie udało się zapisać do pliku {file_path}: {e}")