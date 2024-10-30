# gui_utils.py
import json

def save_checkbox_states(checkbox_list):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        states = {}

    for checkbox in checkbox_list:
        states[checkbox.objectName()] = checkbox.isChecked()

    with open('config.json', 'w') as file:
        json.dump(states, file, indent=4)

def load_checkbox_states(checkbox_list):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)
            for checkbox in checkbox_list:
                checkbox.setChecked(states.get(checkbox.objectName(), False))
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def get_checkbox_state(key):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)
            return states.get(key) 
    except (FileNotFoundError, json.JSONDecodeError):
        return None