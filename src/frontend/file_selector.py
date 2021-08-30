from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import os


window_name, base_class = uic.loadUiType("src/frontend/ui_files/menu.ui")


class Menu(window_name, base_class):
    trigger = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.push_button_ready.clicked.connect(self.continue_to_processing)
        self.push_button_file_selector.clicked.connect(self.path_file_selector)

        # Variables auxiliares de la ventana
        self._excel_path = ""

    @property
    def excel_path(self):
        return self._excel_path

    @excel_path.setter
    def excel_path(self, new_path):
        self._excel_path = new_path

        if len(new_path.split("\\")) > 1:
            new_path = new_path.split("\\")[-1]
        else:
            new_path = new_path.split("/")[-1]

        self.label_path_info.setText("El archivo seleccionado es:")
        self.label_path.setText(new_path)
        self.file_name = new_path

    def continue_to_processing(self):
        self.trigger.emit((self.excel_path, self.file_name))

    def path_file_selector(self):
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
        )
        self.excel_path = response[0]
