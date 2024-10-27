# gui.py
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import sys
import gui_utils  # Importujemy moduł pomocniczy
import utils.building_positions  # Importujemy cały moduł
import control_game.screen_navigation

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)

        # Przypisanie funkcji do przycisku pushButton_config
        self.findChild(QtWidgets.QPushButton, 'pushButton_start').clicked.connect(control_game.screen_navigation.map)
        self.findChild(QtWidgets.QPushButton, 'pushButton_config').clicked.connect(utils.building_positions.buildings_positions)
        

        # Inicjalizacja checkboxów i przypisanie im funkcji
        self.checkbox_list = [self.checkBox_goldmap, 
                              self.checkBox_woodmap, 
                              self.checkBox_stonemap, 
                              self.checkBox_manamap]
        
        for checkbox in self.checkbox_list:
            checkbox.stateChanged.connect(lambda _, boxes=self.checkbox_list: gui_utils.save_checkbox_states(boxes))

        gui_utils.load_checkbox_states(self.checkbox_list)
        self.show()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
