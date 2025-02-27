# gui.py
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import sys
import gui_utils
import utils.buildings.save_position
from task_manager import TaskManager
from utils.general import read_config

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)
        sys.stdout = gui_utils.ConsoleOutput(self.textEdit_logs)
        sys.stderr = gui_utils.ConsoleOutput(self.textEdit_logs)
        self.task_manager = TaskManager()

        # Podłączenie przycisków
        self.findChild(QtWidgets.QPushButton, 'pushButton_start').clicked.connect(self.start_queue_with_delay)
        self.findChild(QtWidgets.QPushButton, 'pushButton_stop').clicked.connect(self.stop_queue)
        self.findChild(QtWidgets.QPushButton, 'pushButton_config').clicked.connect(utils.buildings.save_position.save_position)

        # Podłączenie zmian stanów widżetów
        for checkbox in self.findChildren(QtWidgets.QCheckBox):
            checkbox.stateChanged.connect(self.save_states)
        for lineedit in self.findChildren(QtWidgets.QLineEdit):
            lineedit.editingFinished.connect(self.save_states)
        for combobox in self.findChildren(QtWidgets.QComboBox):
            combobox.currentIndexChanged.connect(self.save_states)
        gui_utils.load_widget_states(self)

        # Autostart, jeśli włączony
        checkBox_autostart = self.findChild(QtWidgets.QCheckBox, 'checkBox_autostart')
        if checkBox_autostart.isChecked():
            self.start_queue_with_delay()
        self.show()

    def save_states(self):
        gui_utils.save_widget_states(self)

    def start_queue(self):
        print("Uruchamiam bota...")
        self.task_manager.start()

    def start_queue_with_delay(self):
        config = read_config()
        delay_str = config.get("lineEdit_delay", "")
        try:
            delay = int(delay_str)
        except ValueError:
            delay = 0
        if delay <= 0:
            self.start_queue()
        else:
            self.remaining_delay = delay
            print(f"Bot wystartuje za: {self.remaining_delay} sekund")
            # Timer odliczania
            self.countdown_timer = QTimer(self)
            self.countdown_timer.timeout.connect(self.update_countdown)
            self.countdown_timer.start(1000)
            # Timer uruchomienia bota
            self.start_timer = QTimer(self)
            self.start_timer.setSingleShot(True)
            self.start_timer.timeout.connect(self.on_start_timer_finished)
            self.start_timer.start(delay * 1000)

    def update_countdown(self):
        self.remaining_delay -= 1
        if self.remaining_delay > 0:
            print(f"Bot wystartuje za: {self.remaining_delay} sekund")
        else:
            self.countdown_timer.stop()

    def on_start_timer_finished(self):
        if hasattr(self, 'countdown_timer'):
            self.countdown_timer.stop()
        self.start_queue()

    def stop_queue(self):
        import threading
        if hasattr(self, 'start_timer') and self.start_timer.isActive():
            self.start_timer.stop()
        if hasattr(self, 'countdown_timer') and self.countdown_timer.isActive():
            self.countdown_timer.stop()
        threading.Thread(target=self.task_manager.stop, daemon=True).start()
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
