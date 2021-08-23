from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random

from backend.peak_finder.signal_processing import get_edi_peaks, get_pes_peaks
from backend.integration.integral import Integration
from frontend.analiser.layout import init_ui


class Analiser(QMainWindow):
    def __init__(self, data_edi, data_pes):
        QMainWindow.__init__(self)

        # Format variables
        self.title = 'Analiser'
        self.left = 10
        self.top = 10
        self.width = 920
        self.height = 580

        # Utility variables
        self.data_edi = data_edi
        self.data_pes = data_pes
        self.integ = Integration(data_edi, data_pes)

        # Add plot 1 to layout
        self.plot_edi = WidgetPlot(self, data=self.data_edi)
         # Add plot 2 to layout
        self.plot_pes = WidgetPlot(
            self, data=self.data_pes, shared_ax=self.plot_edi.canvas.ax)

        init_ui(self)        
        self.showMaximized()

    def edi_button_clicked(self):
        # if self.higher_min_input1.text() != "":
        #     try:
        #         self.integ.higer_min_edi = -float(self.higher_min_input1.text())
        #         self.label_actual_higer_min1.setText(str(-self.integ.higer_min_edi))
        #     except:
        #         pass

        # if self.lower_max_input1.text() != "":
        #     try:
        #         self.integ.lower_max_edi = float(self.lower_max_input1.text())
        #         self.label_actual_lower_max1.setText(str(self.integ.lower_max_edi))
        #     except:
        #         pass

        self.plot_edi.plot_edi_peaks()
        self.plot_edi.canvas.plot_70_points(self.integ.points_70_percent())
        self.plot_edi.canvas.draw()

    def pes_button_clicked(self):

        # if self.higher_min_input2.text() != "":
            # try:
                # self.integ.higer_min_pes = -float(self.higher_min_input2.text())
                # self.label_actual_higher_min2.setText(str(-self.integ.higer_min_pes))
            # except:
                # pass

        # if self.lower_max_input2.text() != "":
            # try:
            #     self.integ.lower_max_pes = float(self.lower_max_input2.text())
            #     self.label_actual_lower_max2.setText(str(self.integ.lower_max_pes))
            # except:
            #     pass

        self.plot_pes.canvas.clean()
        self.plot_pes.plot_pes_peaks()
        self.plot_pes.canvas.plot_70_points(self.integ.points_70_percent())
        self.plot_pes.canvas.plot_integration(self.integ.integration())
        self.plot_pes.canvas.draw()

    def export_data(self):
        pass


class WidgetPlot(QWidget):
    def __init__(self, *args, data, shared_ax=None):
        QWidget.__init__(self, *args)
        self.data = data
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(
            self, width=10, height=8, data=self.data, shared_ax=shared_ax)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        print(args)

    def plot_edi_peaks(self):
        '''
        Plot the peaks of the edi curve stored
        '''
        peaks, antipeaks = get_edi_peaks(self.data)
        self.canvas.edi_peaks_update(peaks, antipeaks)

    def plot_pes_peaks(self):
        '''
        Plot the peaks of the pes curve stored
        '''
        peaks = get_pes_peaks(self.data)
        self.canvas.pes_peaks_update(peaks)




class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, data=[], dpi=100, shared_ax=None):
        # Data variables
        self.data = data

        # Plot variables
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.first_plot(shared_ax)

    def first_plot(self, shared_ax):
        if shared_ax:
            self.ax = self.figure.add_subplot(111, sharex=shared_ax)
        else:
            self.ax = self.figure.add_subplot(111)
        self.ax.plot(self.data, 'r-', linewidth=0.5)
        self.ax.set_title('Edi Signal')
        self.draw()

    def clean(self):
        self.ax.clear()

    def edi_peaks_update(self, peaks, antipeaks):
        self.ax.plot(self.data, 'r-', linewidth=0.5)
        self.ax.plot(peaks, [self.data[x_peak] for x_peak in peaks], 'bo')
        self.ax.plot(antipeaks, [self.data[x_a_peak]
                     for x_a_peak in antipeaks], 'b+')

    def pes_peaks_update(self, peaks):
        self.ax.plot(self.data, 'r-', linewidth=0.5)
        self.ax.plot(peaks, [self.data[x_peak] for x_peak in peaks], 'bo')


    def plot_70_points(self, ind_70):
        '''
        Plot the points where the decreasing pes
        curve, reaches 70%
        '''
        self.ax.plot(ind_70, [self.data[x_peak] for x_peak in ind_70], 'gx')

    def plot_integration(self, int_data):
        for x in int_data:
            # self.ax.axvline(x = x[1], color='b')
            # self.ax.axvline(x = x[2], color='g')
            self.ax.plot([x[1], x[2]],
                [self.data[x[1]], self.data[x[1]]], 'g-')

            self.ax.plot([x[2], x[2]],
                [self.data[x[1]], self.data[x[2]]], 'g-')



