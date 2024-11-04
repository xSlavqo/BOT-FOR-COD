# gui_utils.py
import json
from PyQt5 import QtWidgets


class ConsoleOutput:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.append(text) 

    def flush(self):
        pass  

def save_widget_states(window):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        states = {}

    # Zapisz stany wszystkich QCheckBox
    for checkbox in window.findChildren(QtWidgets.QCheckBox):
        states[checkbox.objectName()] = checkbox.isChecked()

    # Zapisz tekst wszystkich QLineEdit
    for lineedit in window.findChildren(QtWidgets.QLineEdit):
        states[lineedit.objectName()] = lineedit.text()

    # Zapisz dane do pliku JSON
    with open('config.json', 'w') as file:
        json.dump(states, file, indent=4)

def load_widget_states(window):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)

            # Wczytaj stany dla wszystkich QCheckBox
            for checkbox in window.findChildren(QtWidgets.QCheckBox):
                checkbox.setChecked(states.get(checkbox.objectName(), False))

            # Wczytaj tekst dla wszystkich QLineEdit
            for lineedit in window.findChildren(QtWidgets.QLineEdit):
                lineedit.setText(states.get(lineedit.objectName(), ""))
    except (FileNotFoundError, json.JSONDecodeError):
        pass


def get_checkbox_state(key):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)
            return states.get(key) 
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def check_task_conditions(checkbox_names):
    return any(get_checkbox_state(f'checkBox_{name}') for name in checkbox_names)