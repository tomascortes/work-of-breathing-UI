from PyQt5.QtWidgets import  QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random

from backend.peak_finder.signal_processing import get_signal_peaks

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
        self.lower_max_1 = 1.8
        self.higer_min_1 = -1
        self.lower_max_2 = 1.8
        self.higer_min_2 = -1
        self.ventana2 = 150

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
        #-----------------------------------------------------------------
        #-----------------------------------------------------------------

        # Lower max value related
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #Items
        self.label_first_text1 = QLabel('Valor minimo de los maximos:', self)
        self.higer_min_input_1 = QLineEdit(self)
        self.label_actual_higher_min_1 = QLabel(str(self.lower_max_1), self)

        #Placement in layout
        hlay_first.addWidget(self.label_first_text1)
        hlay_first.addWidget(self.higer_min_input_1)
        hlay_first.addWidget(self.label_actual_higher_min_1)
        hlay_first.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        
        vlay.addLayout(hlay_first)
        
        #Higer max related
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_first_text2 = QLabel('Valor maximo de los minimos:', self)
        self.lower_max_input_1 = QLineEdit(self)
        self.label_actual_lower_max_1 = QLabel(str(self.higer_min_1), self)

        #Placement in layout
        hlay_first2 = QHBoxLayout()
        hlay_first2.addWidget(self.label_first_text2)
        hlay_first2.addWidget(self.lower_max_input_1)
        hlay_first2.addWidget(self.label_actual_lower_max_1)
        hlay_first2.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        
        #Button corresponding to first graph
        pybutton_1 = QPushButton('Click me', self)
        aux_layer = QHBoxLayout()
        aux_layer.addWidget(pybutton_1)
        aux_layer.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        first_super_vlay2 = QVBoxLayout()

        first_super_vlay2.addLayout(hlay_first2)
        first_super_vlay2.addLayout(aux_layer)
        vlay.addLayout(first_super_vlay2)

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #Add plot 1 to layout
        self.plot_edi = WidgetPlot(self, data = self.data_edi) 
        vlay.addWidget(self.plot_edi)

        #Second curve realated layouts
        #-----------------------------------------------------------------
        #-----------------------------------------------------------------
        #-----------------------------------------------------------------

        # Lower max value related
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #Items
        self.label_second_text1 = QLabel('Valor minimo de los maximos:', self)
        self.higer_min_input_2 = QLineEdit(self)
        self.label_actual_higher_min_2 = QLabel(str(self.lower_max_1), self)

        #Placement in layout
        hlay_second.addWidget(self.label_second_text1)
        hlay_second.addWidget(self.higer_min_input_2)
        hlay_second.addWidget(self.label_actual_higher_min_2)
        hlay_second.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        
        vlay.addLayout(hlay_second)
        
        #Higer max related
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_second_text2 = QLabel('Valor maximo de los minimos:', self)
        self.lower_max_input_2 = QLineEdit(self)
        self.label_actual_lower_max_2 = QLabel(str(-self.higer_min_1), self)

        #Placement in layout
        hlay_second2 = QHBoxLayout()
        hlay_second2.addWidget(self.label_second_text2)
        hlay_second2.addWidget(self.lower_max_input_2)
        hlay_second2.addWidget(self.label_actual_lower_max_2)
        hlay_second2.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        
        #Button corresponding to second graph
        pybutton_2 = QPushButton('Click me', self)
        aux_layer = QHBoxLayout()
        aux_layer.addWidget(pybutton_2)
        aux_layer.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        second_super_vlay2 = QVBoxLayout()

        second_super_vlay2.addLayout(hlay_second2)
        second_super_vlay2.addLayout(aux_layer)
        vlay.addLayout(second_super_vlay2)

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #Add plot 2 to layout
        self.plot_pes = WidgetPlot(self, data = self.data_pes)
        vlay.addWidget(self.plot_pes)

        #Buttons conections
        pybutton_1.clicked.connect(self.edi_button_clicked)
        pybutton_2.clicked.connect(self.pes_button_clicked)

        self.showMaximized()

    def edi_button_clicked(self):
        if  self.lower_max_input_1.text() != "":
            try:
                self.lower_max_1 = float(self.lower_max_input_1.text())
                self.label_actual_lower_max_1.setText(str(self.lower_max_1))
            except:
                pass

        if  self.higer_min_input_1.text() != "":
            try:
                self.higer_min_1 = float(self.higer_min_input_1.text())
                self.label_actual_higher_min_1.setText(str(self.higer_min_1))
            except:
                pass      

        self.plot_edi.plot_peaks(self.higer_min_1, self.lower_max_1)

    def pes_button_clicked(self):
        if  self.lower_max_input_2.text() != "":
            try:
                self.lower_max_2 = float(self.lower_max_input_2.text())
                self.label_actual_lower_max_2.setText(str(self.lower_max_2))
            except:
                pass

        if  self.higer_min_input_2.text() != "":
            try:
                self.higer_min_2 = float(self.higer_min_input_2.text())
                self.label_actual_higher_min_2.setText(str(self.higer_min_2))
            except:
                pass      

        self.plot_pes.plot_peaks(self.higer_min_2, self.lower_max_2)

        


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

    def plot_peaks(self, lower_max, higer_min):
        peaks, antipeaks = get_signal_peaks(self.data, 0, len(self.data), lower_max, higer_min)
        self.canvas.peaks_update(peaks, antipeaks)
        

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, data=[], dpi=100):
        # Data variables
        self.data = data

        #Plot variables
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

    def peaks_update(self, peaks, antipeaks):
        self.clean()
        self.ax.plot(self.data, 'r-', linewidth = 0.5)
        self.ax.plot(peaks, [self.data[x_peak] for x_peak in peaks], 'bo')
        self.ax.plot(antipeaks, [self.data[x_a_peak] for x_a_peak in antipeaks], 'b+')
        self.draw()