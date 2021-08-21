import sys
from PyQt5.QtWidgets import QApplication
from frontend.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    m = MainWindow()
    sys.exit(app.exec_())
