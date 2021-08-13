from frontend.file_selector import Menu
from frontend.analiser import Analiser
from data_processing.read_data import read_file


class MainWindow:
    def __init__(self):
        self.menu = Menu()
        self.menu.trigger.connect(self.start_analizer)
        self.menu.show()

    def start_analizer(self, path):
        self.path = path
        self.menu.hide()
        data_edi, data_pes = read_file(self.path)
        self.analizer = Analiser(data_edi, data_pes)
        self.analizer.show()
