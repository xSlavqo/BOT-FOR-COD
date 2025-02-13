# gui.py
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer
import sys
import gui_utils
import utils.buildings.save_position
from task_manager import TaskManager


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  
        uic.loadUi('untitled.ui', self)

        sys.stdout = gui_utils.ConsoleOutput(self.textEdit_logs)
        sys.stderr = gui_utils.ConsoleOutput(self.textEdit_logs)

        # Instancja TaskManagera
        self.task_manager = TaskManager()

        # Przyciski start, stop i config
        self.findChild(QtWidgets.QPushButton, 'pushButton_start').clicked.connect(self.start_queue)
        self.findChild(QtWidgets.QPushButton, 'pushButton_stop').clicked.connect(self.stop_queue)
        self.findChild(QtWidgets.QPushButton, 'pushButton_config').clicked.connect(utils.buildings.save_position.save_position)

        # Połącz funkcję zapisu przy zmianie stanu checkboxa lub zakończeniu edycji w QLineEdit
        for checkbox in self.findChildren(QtWidgets.QCheckBox): 
            checkbox.stateChanged.connect(self.save_states)

        for lineedit in self.findChildren(QtWidgets.QLineEdit):
            lineedit.editingFinished.connect(self.save_states)

        for combobox in self.findChildren(QtWidgets.QComboBox):
            combobox.currentIndexChanged.connect(self.save_states)

        # Wczytaj zapisane stany dla wszystkich QCheckBox i QLineEdit
        gui_utils.load_widget_states(self)

        checkBox_autostart = self.findChild(QtWidgets.QCheckBox, 'checkBox_autostart')
        if checkBox_autostart.isChecked():
            self.start_queue_with_delay(1)  # Uruchom z opóźnieniem 10 sekund

        self.show()

    def save_states(self):
        gui_utils.save_widget_states(self)

    def start_queue(self):
        # Rozpoczynamy monitorowanie i wykonywanie zadań
        self.task_manager.start()

    def start_queue_with_delay(self, delay_seconds):
        # Ustawienie opóźnienia przed uruchomieniem kolejki
        QTimer.singleShot(delay_seconds * 1000, self.start_queue)

    def stop_queue(self):
        # Zatrzymujemy monitorowanie i wykonywanie zadań
        self.task_manager.stop()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
