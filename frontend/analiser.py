from PyQt5.QtWidgets import  QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton
from matplotlib.figure import Figure
import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Analiser(QMainWindow):
    def __init__(self, data_edi, data_pes):
        QMainWindow.__init__(self)

        # Format variables
        self.title = 'Analiser'
        self.left = 10
        self.top = 10
        self.width = 920
        self.height = 580
        
        #Utility variables
        self.data_edi = data_edi
        self.data_pes = data_pes
        self.param1 = 3
        self.param2 = 3

        #Extra variables
        self.blue_markers = 'bo'

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage('Ready')

        widget =  QWidget(self)
        self.setCentralWidget(widget)
        vlay = QVBoxLayout(widget)
        hlay_first = QHBoxLayout()
        hlay_second = QHBoxLayout()


        #First curve realated layout
        vlay.addLayout(hlay_first)

        #Items
        self.label_first_text = QLabel('Parametro de peaks:', self)
        self.line = QLineEdit(self)
        self.label_actual_parameter = QLabel('Result', self)

        #Placement in layout
        hlay_first.addWidget(self.label_first_text)
        hlay_first.addWidget(self.line)
        hlay_first.addWidget(self.label_actual_parameter)
        hlay_first.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        
        #Button corresponding to first graph
        pybutton1 = QPushButton('Click me', self)
        hlay_first_button = QHBoxLayout()
        hlay_first_button.addWidget(pybutton1)
        hlay_first_button.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        vlay.addLayout(hlay_first_button)

        #Add plot 1 to layout
        self.plot_edi = WidgetPlot(self, data = self.data_edi) 
        vlay.addWidget(self.plot_edi)

        #Second curve realated layouts
        vlay.addLayout(hlay_second)

        #Items
        self.label_second_text = QLabel('Parametro de peaks:', self)
        self.line = QLineEdit(self)
        self.label_actual_parameter = QLabel('Result', self)

        #Placement in layout
        hlay_second.addWidget(self.label_second_text)
        hlay_second.addWidget(self.line)
        hlay_second.addWidget(self.label_actual_parameter)
        hlay_second.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        
        #Button corresponding to second graph
        pybutton2 = QPushButton('Click me', self)
        hlay_second_button = QHBoxLayout()
        hlay_second_button.addWidget(pybutton2)
        hlay_second_button.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        vlay.addLayout(hlay_second_button)

        #Add plot 2 to layout
        self.plot_pes = WidgetPlot(self, data = self.data_pes)
        vlay.addWidget(self.plot_pes)

        #Buttons conections
        pybutton1.clicked.connect(
            lambda: self.plot_edi.canvas.plot_dot(self.param1, self.blue_markers))
        
        pybutton2.clicked.connect(
            lambda: self.plot_pes.canvas.peaks_update(self.param2))

        self.showMaximized()


class WidgetPlot(QWidget):
    def __init__(self, *args, data):
        QWidget.__init__(self, *args)
        self.data = data
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self, width=10, height=8, data=self.data)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        print(args)    

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, data=[], dpi=100):
        self.data = data
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.first_plot()

    def first_plot(self):
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(self.data, 'r-', linewidth = 0.5)
        self.ax.set_title('PyQt Matplotlib Example')
        self.draw()

    def plot_dot(self, param, c):
        self.ax.plot([200], [param], c)
        self.draw()

    def clean(self):
        self.ax.clear()

    def peaks_update(self, param):
        self.clean()
        self.ax.plot(self.data, 'r-', linewidth = 0.5)
        self.ax.plot([i*20 for i in range(1000)], [random.randint(2,20) for _ in range(1000)], 'bo')
        self.draw()

        





