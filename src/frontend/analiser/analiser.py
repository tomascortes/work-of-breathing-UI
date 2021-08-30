from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QSizePolicy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from src.backend.peak_finder.signal_processing import get_edi_peaks, get_pes_peaks
from src.backend.integration.integral import Integration
from src.data_manage.output_data import create_excel
from src.frontend.analiser.layout import init_ui


class Analiser(QMainWindow):
    def __init__(self, data_edi, data_pes, f_name):
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
        self.integ_results = None
        self.file_name = f_name

        # Add plot 1 to layout
        self.plot_edi = WidgetPlot(self, data=self.data_edi)
        # Add plot 2 to layout
        self.plot_pes = WidgetPlot(
            self, data=self.data_pes, shared_ax=self.plot_edi.canvas.ax)

        init_ui(self)
        self.showMaximized()

    def edi_button_clicked(self):
        if self.big_sigma_input1.text() != "":
            try:
                self.integ.big_sigma_edi = float(self.big_sigma_input1.text())
                self.lable_actual_big_sigma1.setText(
                    str(self.integ.big_sigma_edi))
            except:
                pass

        # if self.small_sigma_edit1.text() != "":
        #     try:
        #         self.integ.small_sigma_edi = float(self.small_sigma_edit1.text())
        #         self.label_actual_small_sigma1.setText(str(self.integ.small_sigma_edi))
        #     except:
        #         pass
        # Values getted
        peaks, antipeaks, smoothed_edi = get_edi_peaks(self.data_edi,
                                                       big_sigma=self.integ.big_sigma_edi)

        # Ploting
        self.plot_edi.canvas.clean()
        if self.check_box_smooth_1.isChecked():
            self.plot_edi.canvas.plot_smoothed_edi(smoothed_edi)
        self.plot_edi.canvas.plot_raw_data()
        self.plot_edi.canvas.edi_peaks_update(peaks, antipeaks)
        self.plot_edi.canvas.plot_75_points(self.integ.points_75_percent())
        self.plot_edi.canvas.draw()

    def pes_button_clicked(self):

        if self.big_sigma_input2.text() != "":
            try:
                self.integ.big_sigma_pes = float(self.big_sigma_input2.text())
                self.label_actual_big_sigma2.setText(
                    str(self.integ.big_sigma_pes))
            except:
                pass

        if self.small_sigma_input2.text() != "":
            try:
                self.integ.small_sigma_pes = float(
                    self.small_sigma_input2.text())
                self.label_actual_small_sigma2.setText(
                    str(self.integ.small_sigma_pes))
            except:
                pass
        # values getted
        peaks, big_smoothing, small_smoothing = get_pes_peaks(self.data_pes,
                                                              big_sigma=self.integ.big_sigma_pes,
                                                              small_sigma=self.integ.small_sigma_pes)
        self.integ_results = self.integ.integration()

        # Ploting
        self.plot_pes.canvas.clean()
        if self.check_box_smooth_2.isChecked():
            self.plot_pes.canvas.plot_smoothed_pes(
                big_smoothing, small_smoothing)
        self.plot_pes.canvas.plot_raw_data()
        self.plot_pes.canvas.pes_peaks_update(peaks)
        self.plot_pes.canvas.plot_75_points(self.integ.points_75_percent())

        self.plot_pes.canvas.plot_integration(self.integ_results)
        self.plot_pes.canvas.draw()

    def export_data(self):
        peaks, antipeaks, _ = get_edi_peaks(self.data_edi,
                                            big_sigma=self.integ.big_sigma_edi)
        self.integ_results = self.integ.integration()
        create_excel(self.integ_results, peaks,
                     antipeaks, f_name=self.file_name)


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

    def plot_raw_data(self):
        self.ax.plot(self.data, 'r-', linewidth=0.5)

    def edi_peaks_update(self, peaks, antipeaks):
        self.ax.plot(peaks, [self.data[x_peak] for x_peak in peaks], 'bo')
        self.ax.plot(antipeaks, [self.data[x_a_peak]
                     for x_a_peak in antipeaks], 'b+')

    def pes_peaks_update(self, peaks):
        self.ax.plot(peaks, [self.data[x_peak] for x_peak in peaks], 'bo')

    def plot_75_points(self, ind_75):
        '''
        Plot the points where the decreasing pes
        curve, reaches 75%
        '''
        self.ax.plot(ind_75, [self.data[x_peak] for x_peak in ind_75], 'gx')

    def plot_integration(self, int_data):
        c = 0
        for x in int_data:
            self.ax.plot([x[1], x[2]],
                         [self.data[x[1]], self.data[x[1]]], 'g-')

            self.ax.plot([x[2], x[2]],
                         [self.data[x[1]], self.data[x[2]]], 'g-')

            tx = (x[1] + x[2])/2
            ty = (self.data[x[1]] + self.data[x[1]])/2

            self.ax.annotate(str(c), xy=(tx, ty))
            c += 1

    def plot_smoothed_edi(self, smoothed_edi):
        self.ax.plot(smoothed_edi, 'y-')

    def plot_smoothed_pes(self, big_smoothing, small_smoothing):
        self.ax.plot(big_smoothing, 'y-')
        self.ax.plot(small_smoothing, 'c-')
