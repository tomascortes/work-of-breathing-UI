
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks

from src.data_manage.read_data import read_file


def get_edi_peaks_old(data, big_sigma=300, dist_from_pl=0, dist=75, prom=1) -> tuple:
    """receives a list with a edi signal, find its peaks and valleys (antipeaks),
    returning it as a tuple of the arrays of positions of the peaks in the data with 
    the smoothed curve.
    big_sigma: The function calculates all peaks over and antipeaks under a filtered
    version of the signal (with sigma big_sigma) plus dist_from_pl.
    dist: minimum distance between peaks
    prom: minimum prominence (vertical distance between the peak and its lowest contour line)
    of peaks
    """
    # xs corresponds to x coordinates and ys to the signal values
    ys = np.array(data)
    # peak limits obtained from smoothed signal
    peak_lims = gaussian_filter(ys, big_sigma)
    # positions for positive peaks (local maxima)
    peaks, _ = find_peaks(ys, height=(
        peak_lims + dist_from_pl, np.amax(ys)), distance=dist, prominence=prom)
    # positions for negative peaks (local minima)
    antipeaks, _ = find_peaks(-ys, height=(-peak_lims + dist_from_pl,
                              np.amax(-ys)), distance=dist, prominence=prom)

    return (peaks, antipeaks, peak_lims)

def get_edi_peaks(data, smoothing_sigma=2.1, big_sigma=300, small_sigma=25, dist_from_pl=0, dist=75, prom=1) -> tuple:
    """receives a list with a edi signal, find its peaks and valleys (antipeaks),
    returning it as a tuple of the arrays of positions of the peaks in the data with 
    the smoothed curve.
    big_sigma: The function calculates all peaks over and antipeaks under a filtered
    version of the signal (with sigma big_sigma) plus dist_from_pl.
    dist: minimum distance between peaks
    prom: minimum prominence (vertical distance between the peak and its lowest contour line)
    of peaks
    """
    # xs corresponds to x coordinates and ys to the signal values
    ys = np.array(data)
    # peak limits obtained from smoothed signal
    peak_lims = gaussian_filter(ys, big_sigma)
    # positions for positive peaks (local maxima)
    peaks, _ = find_peaks(ys, height=(
        peak_lims + dist_from_pl, np.amax(ys)), distance=dist, prominence=prom)
    # positions for negative peaks (local minima)
    antipeaks, smoothed_sgnl, very_smoothed_sgnl, less_smoothed_sgnl = get_edi_antipeaks(
        data, smoothing_sigma=smoothing_sigma, big_sigma=big_sigma, small_sigma=small_sigma, dist_from_pl=dist_from_pl)

    return (peaks, antipeaks, very_smoothed_sgnl, less_smoothed_sgnl)

def get_edi_antipeaks(data, smoothing_sigma =2.1, big_sigma=300, small_sigma=25, dist_from_pl=0, dist=1, prom=0) -> tuple:
    """receives a list with a edi signal, and find the local valley just
    before the the cycles starts ascending to its peak.
    Works the same as get_pes_peaks() but with an inverted edi signal.
    Returns numpy array of x-axis positions of antipeaks in signal.
    smoothing_sigma: the initial data is smoothed with sigma smoothing_sigma before finding the peaks.
    big_sigma and small_sigma: The function returns the first peaks before each inflection point
    of the signal, wich are aproximated as the intersection of a smoothed version of the origianl
    signal with sigma big_sigma and other version smoothed with small_sigma.
    dist_from_pl: will not return any peaks under smoothed signal with big_sigma + dist_from_pl.
    dist: minimum distance between peaks
    prom: minimum prominence (vertical distance between the peak and its lowest contour line) of peaks
    """
    # xs corresponds to x coordinates and ys to the signal values
    ys = -np.array(data)
    # smoothed signal to find the peaks in
    smoothed_sgnl = gaussian_filter(ys, smoothing_sigma)
    # signal smoothed with big_sigma
    very_smoothed_sgnl = gaussian_filter(ys, big_sigma)
    # signal smoothed with small_sigma
    less_smoothed_sgnl = gaussian_filter(ys, small_sigma)
    # positions for antipeaks (local minima)
    antipeaks, _ = find_peaks(smoothed_sgnl, height=(
        very_smoothed_sgnl + dist_from_pl, np.amax(ys)), distance=dist, prominence=prom)

    # Positive when signal in mount, negative in valley:
    mount_or_valley = np.sign(less_smoothed_sgnl - very_smoothed_sgnl)
    # Positions where curve less_smoothed_signl crosses curve very_smoothed_sgnl
    inflection_points = np.where(np.diff(mount_or_valley))[0]
    # Whe get the positions of only the valley crossings
    if mount_or_valley[0] > 0:
        valley_crossings = inflection_points[::2]
    else:
        valley_crossings = inflection_points[1::2]

    cnt = 0
    edi_antipeaks = []
    v_c_len = len(valley_crossings)
    for i, peak in enumerate(antipeaks):
        if peak >= valley_crossings[cnt]:
            edi_antipeaks.append(antipeaks[i-1])
            cnt += 1
            if cnt == v_c_len:
                break

    return (edi_antipeaks, smoothed_sgnl, very_smoothed_sgnl, less_smoothed_sgnl)

def get_pes_peaks(data, big_sigma=300, small_sigma=25, dist_from_pl=0, dist=1, prom=0.07) -> tuple:
    """receives a list with a pes signal, and find the local peaks just
    before the the cycles starts decending to its valley.
    Returns numpy array of x-axis positions of peaks in signal, 
    the very smoothed curve and the less smoothed curve.
    big_sigma and small_sigma: The function returns the first peaks before each inflection point
    of the signal, wich are aproximated as the intersection of a smoothed version of the origianl
    signal with sigma big_sigma and other version smoothed with small_sigma.
    dist_from_pl: will not return any peaks under smoothed signal with big_sigma + dist_from_pl.
    dist: minimum distance between peaks
    prom: minimum prominence (vertical distance between the peak and its lowest contour line) of peaks
    """
    # xs corresponds to x coordinates and ys to the signal values
    ys = np.array(data)
    # signal smoothed with big_sigma
    very_smoothed_sgnl = gaussian_filter(ys, big_sigma)
    # signal smoothed with small_sigma
    less_smoothed_sgnl = gaussian_filter(ys, small_sigma)
    # positions for positive peaks (local maxima)
    peaks, _ = find_peaks(ys, height=(
        very_smoothed_sgnl + dist_from_pl, np.amax(ys)), distance=dist, prominence=prom)
    # positions for negative peaks (local minima)
    # antipeaks, _ = find_peaks(-ys, height=(-very_smoothed_sgnl + dist_from_pl, np.amax(-ys)))
    # Positive when signal in mount, negative in valley:
    mount_or_valley = np.sign(less_smoothed_sgnl - very_smoothed_sgnl)
    # Positions where curve less_smoothed_signl crosses curve very_smoothed_sgnl
    inflection_points = np.where(np.diff(mount_or_valley))[0]
    # Whe get the positions of only the valley crossings
    if mount_or_valley[0] > 0:
        valley_crossings = inflection_points[::2]
    else:
        valley_crossings = inflection_points[1::2]

    cnt = 0
    pes_peaks = []
    v_c_len = len(valley_crossings)
    for i, peak in enumerate(peaks):
        if peak >= valley_crossings[cnt]:
            pes_peaks.append(peaks[i-1])
            cnt += 1
            if cnt == v_c_len:
                break

    return (pes_peaks, very_smoothed_sgnl, less_smoothed_sgnl)

# New functions 1/11/2021:
class SignalProcessor:
    """
    Class for all signal processing functionality.
    * Inputs:
        data:                   array of signal data.
        smoothing_sigma:        the initial data is smoothed with sigma smoothing_sigma before finding the straight_peaks.
        big_sigma:              positions are considered peaks or antipeaks if they are found over or under the signal smoothed with big_sigma.
        dist_from_pl:           will not return any peaks or antipeaks in smoothed signal with big_sigma +- dist_from_pl o.
        dist:                   minimum distance between straight peaks or antipeaks.
        prom:                   minimum prominence for straigt_peaks(vertical distance between the peak and its lowest contour line) of peaks or antipeaks.
    """
    def __init__(self, data, smoothing_sigma=2.1, big_sigma=300, small_sigma=25, dist_from_pl=0, dist=75,  prom=1):
        # self.signal corresponds to an array of the signal values
        self.signal = np.array(data)
        # smoothed signal with smoothing_sigma to ignore noise-derived peaks
        self.smoothed_signal = self.get_smoothed_signal(self.signal, smoothing_sigma)
        # signal smoothed with big_sigma
        self.big_smoothed_signal = self.get_smoothed_signal(self.signal, big_smoothing_sigma)
        # signal smoothed with small_sigma
        self.small_smoothed_signal = self.get_smoothed_signal(self.signal, small_smoothing_sigma)
        
        # Values for calculating straight_signal_peaks
        self.dist_from_pl = dist_from_pl
        self.dist = dist
        self.prom = prom


        # ALL positions for positive peaks (local maxima)
        self.all_peaks, _ = find_peaks(self.smoothed_signal, height=(
            self.big_smoothed_signal + self.dist_from_pl, np.amax(self.signal)), distance=1)
        # ALL positions for negative peaks (local minima)
        self.all_antipeaks, _ = find_peaks(-self.smoothed_signal, height=(
            -self.big_smoothed_signal + self.dist_from_pl, np.amax(-self.signal)), distance=1)

        self.ip_pos, self.ip_neg = self.get_inflection_points()

        # array of positions of first local maxima of each mount of the signal.
        self.left_peaks = self.get_sided_peaks(side="left")
        # array of positions of last local maxima of each mount of the signal.
        self.right_peaks = self.get_sided_peaks(side="right")
        # array of positions of first local minima of each valley of the signal.
        self.left_antipeaks = self.get_sided_peaks(side = "left", antipeak = True)
        # array of positions of last local minima of each valley of the signal.
        self.right_antipeaks = self.get_sided_peaks(side = "right", antipeak = True)

    def get_smoothed_signal(self, smoothing_sigma) -> list:
        """
        Returns a smoothed version of original signal data, filtered with a gaussian filter with sigma smoothing_sigma
        """

        return gaussian_filter(self.signal, smoothing_sigma)

    def get_straight_signal_peaks(self, antipeak = False) -> tuple:
        """
        Returns tuple of arrays of positions of local maxima or minima of each cycle of the signal.
        """

        if not antipeak:
            # positions for positive peaks (local maxima)
            peaks, _ = find_peaks(self.smoothed_signal, height=(
                self.very_smoothed_sgnl + self.dist_from_pl, np.amax(self.signal)), distance=self.dist, prominence=self.prom)
        else:
            # positions for negative peaks (local minima)
            peaks, _ = find_peaks(-self.smoothed_signal, height=(
                -self.very_smoothed_sgnl + self.dist_from_pl, np.amax(-self.signal)), distance=self.dist, prominence=self.prom)

        return peaks

    def get_inflection_points(self) -> tuple:
        """
        Returns two arrays of x positions of inflection points of the signal, estimated as the intersections between
            the original signal smoothed with sigma big_sigma and sigma small_sigma. First array is when derivative is
            positive, second is when first derivative is negative.
        """

        # Positive when signal in mount, negative in valley:
        mount_or_valley = np.sign(self.small_smoothed_signal - self.big_smoothed_signal)
        # Positions where curve less_smoothed_signl crosses curve very_smoothed_sgnl
        inflection_points = np.where(np.diff(mount_or_valley))[0]
        # Whe get the x positions of the intersections when derivative is positive or negative
        if mount_or_valley[0] > 0:
            inflection_points_pos_der = inflection_points[::2]
            inflection_points_neg_der = inflection_points[1::2]
        else:
            inflection_points_pos_der = inflection_points[1::2]
            inflection_points_neg_der = inflection_points[::2]

        return (inflection_points_pos_der, inflection_points_neg_der)

    def get_sided_peaks(self, side, antipeak = False) -> list:
        """
        Returns array of positions of first local peak of each valley/mount of the signal, coming from side "side".
        """
        if antipeak:
            all_peaks = self.all_antipeaks
        else:
            all_peaks = self.all_peaks
        
        sc_len = len(inflection_points)
        peaks = []
        cnt = 0
        if side == "right":
            inflection_points = self.ip_neg
            for i, peak_xpos in enumerate(all_peaks):
                if peak_xpos >= inflection_points[cnt]:
                    peaks.append(all_peaks[i-1])
                    cnt += 1
                    if cnt == sc_len:
                        break
        elif side == "left":
            inflection_points = self.ip_pos
            all_peaks = all_peaks[::-1]
            inflection_points = inflection_points[::-1]
            for i, peak_xpos in enumerate(all_peaks):
                if peak_xpos <= inflection_points[cnt]:
                    peaks.append(all_peaks[i-1])
                    cnt += 1
                    if cnt == sc_len:
                        break
            peaks = peaks[::-1]
        
        return peaks


if __name__ == '__main__':
    # positions for positive peaks (local maxima)
    path = ".../../data/01_ PVE 1_Importacion de datos filtrados_con graficos.xlsm"
    edi, pes = read_file(path)
