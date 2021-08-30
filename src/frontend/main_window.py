from src.frontend.file_selector import Menu
from src.frontend.analiser.analiser import Analiser
from src.data_manage.read_data import read_file


class MainWindow:
    def __init__(self):
        self.menu = Menu()
        self.menu.trigger.connect(self.start_analizer)
        self.menu.show()

    def start_analizer(self, path):
        self.path = path[0]
        filename = path[1]
        self.menu.hide()
        data_edi, data_pes = read_file(self.path)
        self.analizer = Analiser(data_edi, data_pes, filename)
        self.analizer.show()
