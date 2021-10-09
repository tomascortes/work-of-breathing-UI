from PyQt5.QtWidgets import  QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import os



class Menu(QMainWindow):
    trigger = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.init_layout()

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

    def init_layout(self):
        self.setWindowTitle("Selección archivo")
        self.setGeometry(50, 50, 500, 700)
        self.statusBar().showMessage('')

        widget = QWidget(self)
        self.setCentralWidget(widget)

        hlay = QHBoxLayout(widget)
        hlay.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        vlay = QVBoxLayout()
        self.label_instructions = QLabel('Seleccione el archivo excel a utilizar', self)
        self.push_button_file_selector = QPushButton('Abrir archivo', self)
        self.label_path_info = QLabel('No hay archivo seleccionado', self)
        self.label_path = QLabel('', self)
        self.push_button_ready = QPushButton('Continuar', self)

        vlay.addWidget(self.label_instructions)
        vlay.addWidget(self.push_button_file_selector)
        vlay.addWidget(self.label_path_info)
        vlay.addWidget(self.label_path)
        vlay.addWidget(self.push_button_ready)
        vlay.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))



        hlay.addLayout(vlay)
        hlay.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
