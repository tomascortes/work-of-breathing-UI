from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QSizePolicy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from src.backend.peak_finder.signal_processing import get_edi_peaks_old, SignalProcessor
from src.backend.integration.integral import Integration
from src.data_manage.output_data import create_excel, create_excel_without_edi
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
        self.sp_edi = SignalProcessor(data_edi)
        self.sp_pes = SignalProcessor(data_pes)
        self.integ = Integration(data_edi, data_pes, self.sp_edi, self.sp_pes)
        self.integ_results_pes = None
        self.file_name = f_name

        # Add plot 1 to layout
        self.plot_edi = WidgetPlot(self, data=self.data_edi)
        # Add plot 2 to layout
        self.plot_pes = WidgetPlot(
            self, data=self.data_pes, shared_ax=self.plot_edi.canvas.ax)

        self.plot_edi.canvas.ax.set_title('Edi Signal')
        self.plot_pes.canvas.ax.set_title('Pes Signal')

        init_ui(self)
        self.showMaximized()

    def button_calculate_clicked(self):

        self.edi_input_update()
        self.pes_input_update()

        if not self.check_box_integration_method.isChecked():
            integ_edi, integ_pes = self.integ.coordinated_integrals()
            self.integ_results_edi = integ_edi
            self.integ_results_pes = integ_pes

            self.edi_ploting()
            self.pes_ploting()
        else:
            integ_pes = self.integ.integration_pes_without_edi()
            self.integ_results_pes = integ_pes
            self.pes_ploting()


    def edi_input_update(self):
        if self.big_sigma_input1.text() != "":
            try:
                self.integ.big_sigma_edi = float(self.big_sigma_input1.text())
                self.lable_actual_big_sigma1.setText(
                    str(self.integ.big_sigma_edi))
            except:
                pass

        if self.small_sigma_input1.text() != "":
            try:
                self.integ.small_sigma_edi = float(
                    self.small_sigma_input1.text())
                self.label_actual_small_sigma1.setText(
                    str(self.integ.small_sigma_edi))
            except:
                pass
        if self.integ.small_sigma_edi == self.integ.big_sigma_edi:
            self.integ.big_sigma_edi += 3

    def edi_ploting(self):
        # Values getted
        if self.check_peak_method.isChecked():
            self.integ.old_edi_method = True
            peaks, antipeaks, b_smooth = get_edi_peaks_old(
                self.data_edi,
                big_sigma=self.integ.big_sigma_edi)
            s_smooth = []
        else:
            self.integ.old_edi_method = False

            self.sp_edi.update_peaks(
                big_sigma=self.integ.big_sigma_edi,
                small_sigma=self.integ.small_sigma_edi)

            peaks = self.sp_edi.get_straight_signal_peaks()
            antipeaks = self.sp_edi.right_antipeaks
            b_smooth = self.sp_edi.big_smoothed_signal
            s_smooth = self.sp_edi.small_smoothed_signal

        # Ploting
        self.plot_edi.canvas.clean()
        if self.check_box_smooth_1.isChecked():
            self.plot_edi.canvas.plot_smoothed(b_smooth, s_smooth)

        self.plot_edi.canvas.plot_raw_data()
        self.plot_edi.canvas.edi_peaks_update(peaks, antipeaks)
        self.plot_edi.canvas.plot_75_points(self.integ.points_75_percent())
        self.plot_edi.canvas.plot_integration(self.integ_results_edi)
        self.plot_edi.canvas.ax.set_title('Edi Signal')
        self.plot_edi.canvas.draw()

    def pes_input_update(self):
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

        if self.integ.small_sigma_pes == self.integ.big_sigma_pes:
            self.integ.big_sigma_pes += 3

    def pes_ploting(self):
        self.sp_pes.update_peaks(
            big_sigma=self.integ.big_sigma_pes,
            small_sigma=self.integ.small_sigma_pes)

        # values getted
        peaks = self.sp_pes.right_peaks
        big_smoothing = self.sp_pes.big_smoothed_signal
        small_smoothing = self.sp_pes.small_smoothed_signal

        # Ploting
        self.plot_pes.canvas.clean()
        if self.check_box_smooth_2.isChecked():
            self.plot_pes.canvas.plot_smoothed(
                big_smoothing, small_smoothing)
        self.plot_pes.canvas.plot_raw_data()
        self.plot_pes.canvas.pes_peaks_update(peaks)
        if not self.check_box_integration_method.isChecked():
            self.plot_pes.canvas.plot_75_points(self.integ.points_75_percent())


        self.plot_pes.canvas.plot_integration(self.integ_results_pes)
        self.plot_pes.canvas.ax.set_title('Pes Signal')
        self.plot_pes.canvas.draw()

    def export_data(self):
        self.statusBar().showMessage("Exportando")

        if not self.check_box_integration_method.isChecked():

            self.sp_edi.update_peaks(
                big_sigma=self.integ.big_sigma_edi,
                small_sigma=self.integ.small_sigma_edi)

            peaks = self.sp_edi.get_straight_signal_peaks()
            antipeaks = self.sp_edi.right_antipeaks
            integ_edi, integ_pes = self.integ.coordinated_integrals()
            self.integ_results_edi = integ_edi
            self.integ_results_pes = integ_pes

            create_excel(
                self.integ_results_pes,
                self.integ_results_edi,
                peaks,
                antipeaks,
                f_name=self.file_name)
        else:
            integ_pes = self.integ.integration_pes_without_edi()
            self.integ_results_pes = integ_pes
            create_excel_without_edi(integ_pes)
        self.statusBar().showMessage(f'Archivo {self.file_name} exportado')


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

    def plot_smoothed(self, big_smoothing, small_smoothing):
        self.ax.plot(big_smoothing, 'y-')
        self.ax.plot(small_smoothing, 'c-')
