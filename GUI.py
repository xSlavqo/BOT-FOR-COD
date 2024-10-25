# gui.py
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import sys
import gui_utils  # Importujemy moduł pomocniczy

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)

        self.checkbox_list = [self.checkBox_goldmap, 
                              self.checkBox_woodmap, 
                              self.checkBox_stonemap, 
                              self.checkBox_manamap]
        
        for checkbox in self.checkbox_list:
            checkbox.stateChanged.connect(self.save_checkbox_states)

        self.load_checkbox_states()
        self.show()

    def save_checkbox_states(self):
        gui_utils.save_checkbox_states(self.checkbox_list)

    def load_checkbox_states(self):
        gui_utils.load_checkbox_states(self.checkbox_list)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
