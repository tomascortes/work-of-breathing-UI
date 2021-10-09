import sys
from PyQt5.QtWidgets import QApplication
from src.frontend.main_window import MainWindow

def main():
    app = QApplication([])
    m = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()