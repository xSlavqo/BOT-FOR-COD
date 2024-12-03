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

    # Zapisz stany wszystkich QCheckBox
    for checkbox in window.findChildren(QtWidgets.QCheckBox):
        states[checkbox.objectName()] = checkbox.isChecked()

    # Zapisz tekst wszystkich QLineEdit
    for lineedit in window.findChildren(QtWidgets.QLineEdit):
        states[lineedit.objectName()] = lineedit.text()

    # Zapisz wybrany indeks wszystkich QComboBox
    for combobox in window.findChildren(QtWidgets.QComboBox):
        states[combobox.objectName()] = combobox.currentIndex()

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

            # Wczytaj wybrany indeks dla wszystkich QComboBox
            for combobox in window.findChildren(QtWidgets.QComboBox):
                combobox.setCurrentIndex(states.get(combobox.objectName(), 0))
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

def get_combobox_state(key):
    try:
        with open('config.json', 'r') as file:
            states = json.load(file)
            return states.get(key)  # Zwróć indeks zapisany w config.json
    except (FileNotFoundError, json.JSONDecodeError):
        return None  # Zwróć None, jeśli brak danych
