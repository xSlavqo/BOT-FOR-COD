# gui.py
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import sys
import threading
import gui_utils
import utils.building_positions
import task_manager  # Zmieniony import na task_manager

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)

        # sys.stdout = gui_utils.ConsoleOutput(self.textEdit_logs)
        # sys.stderr = gui_utils.ConsoleOutput(self.textEdit_logs)
        
        self.stop_event = threading.Event()
        
        # Przyciski start, stop i config
        self.findChild(QtWidgets.QPushButton, 'pushButton_start').clicked.connect(self.start_queue)
        self.findChild(QtWidgets.QPushButton, 'pushButton_stop').clicked.connect(self.stop_queue)
        self.findChild(QtWidgets.QPushButton, 'pushButton_config').clicked.connect(utils.building_positions.buildings_positions)

        # Połącz funkcję zapisu przy zmianie stanu checkboxa lub zakończeniu edycji w QLineEdit
        for checkbox in self.findChildren(QtWidgets.QCheckBox):
            checkbox.stateChanged.connect(self.save_states)

        for lineedit in self.findChildren(QtWidgets.QLineEdit):
            lineedit.editingFinished.connect(self.save_states)

        # Wczytaj zapisane stany dla wszystkich QCheckBox i QLineEdit
        gui_utils.load_widget_states(self)

        self.show()

    def save_states(self):
        gui_utils.save_widget_states(self)

    def start_queue(self):
        self.stop_event.clear()
        task_manager.start_task_execution(self.stop_event)  # Uruchamiamy kolejkę i monitorowanie zadań

    def stop_queue(self):
        self.stop_event.set()  # Zatrzymujemy kolejkę i monitorowanie zadań

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
