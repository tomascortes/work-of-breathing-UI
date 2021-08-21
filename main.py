import sys
from PyQt5.QtWidgets import QApplication
from frontend.main_window import MainWindow

if __name__ == "__main__":

    path = "./data/01_ PVE 1_Importacion de datos filtrados_con graficos.xlsm"
    app = QApplication([])
    m = MainWindow()
    sys.exit(app.exec_())
