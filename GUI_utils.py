# gui_utils.py
import json
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

class ConsoleOutput(QObject):
    new_text = pyqtSignal(str)  # Sygnał do przekazania tekstu do widgetu

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.new_text.connect(self.widget.append)  # Połącz sygnał z metodą `append`

    def write(self, text):
        if text.strip():  # Ignoruj puste linie
            self.new_text.emit(text.strip())  # Emituj sygnał z nowym tekstem

    def flush(self):
        pass  # Wymuszamy przepływ danych na bieżąco (nie zostawiamy pustej metody)


def save_widget_states(window):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        states = {}

    for checkbox in window.findChildren(QtWidgets.QCheckBox):
        states[checkbox.objectName()] = checkbox.isChecked()

    for lineedit in window.findChildren(QtWidgets.QLineEdit):
        states[lineedit.objectName()] = lineedit.text()

    for combobox in window.findChildren(QtWidgets.QComboBox):
        states[combobox.objectName()] = combobox.currentIndex()

    with open('config.json', 'w') as file:
        json.dump(states, file, indent=4)


def load_widget_states(window):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        states = {}

    for checkbox in window.findChildren(QtWidgets.QCheckBox):
        if checkbox.objectName() in states:
            checkbox.setChecked(states[checkbox.objectName()])

    for lineedit in window.findChildren(QtWidgets.QLineEdit):
        if lineedit.objectName() in states:
            lineedit.setText(states[lineedit.objectName()])

    for combobox in window.findChildren(QtWidgets.QComboBox):
        if combobox.objectName() in states:
            combobox.setCurrentIndex(states[combobox.objectName()])



def get_checkbox_state(key):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)
            return states.get(key) 
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def check_task_conditions(checkbox_names):
    return any(get_checkbox_state(f'checkBox_{name}') for name in checkbox_names)

def get_combobox_state(key):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)
            return states.get(key)  # Zwróć indeks zapisany w config.json
    except (FileNotFoundError, json.JSONDecodeError):
        return None  # Zwróć None, jeśli brak danych
