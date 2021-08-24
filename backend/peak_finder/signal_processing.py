
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks
from data_reading.read_data import read_file


# def get_signal_peaks(data, min_max, max_min, first_dp=0, last_dp=None, dist=150) -> tuple:
#     """recives a list with a signal, and tries to find its peaks and valleys (antipeaks),
#     returning it as a tuple o the arrays of positions of the peaks in the data.
#     """
#     if not last_dp:
#         last_dp = len(data)
#     # xs corresponds to x coordinates and ys to the signal values
#     xs, ys = np.arange(last_dp-first_dp), np.array(data[first_dp:last_dp])

#     # Signal "energy"
#     # yss = np.square(ys)

#     # smooth out noise
#     # smoothed = gaussian_filter(ys, 3.)

#     # peak limits obtained from smoothed signal
#     # peak_lims = gaussian_filter(ys, 300)

#     # positions for positive peaks (local maxima)
#     peaks, _ = find_peaks(ys, height=(min_max, np.amax(ys)), distance=dist)
#     # positions for negative peaks (local minima)
#     antipeaks, _ = find_peaks(-ys, height=(-max_min, np.amax(-ys)), distance=dist)

#     return (peaks, antipeaks)

def get_edi_peaks(data, smoothing_sigma = 300, dist_from_pl = 0, dist = 70, prom = 1) -> tuple:
    """receives a list with a edi signal, and tries to find its peaks and valleys (antipeaks),
    returning it as a tuple of the arrays of positions of the peaks in the data.
    smoothing_sigma: The function calculates all peaks over and antipeaks under a filtered
    version of the signal (with sigma smoothing_sigma) plus dist_from_pl.
    dist: minimum distance between peaks
    prom: minimum prominence (vertical distance between the peak and its lowest contour line)
    of peaks
    """
    # xs corresponds to x coordinates and ys to the signal values
    ys = np.array(data)
    # peak limits obtained from smoothed signal
    peak_lims = gaussian_filter(ys, smoothing_sigma)
    # positions for positive peaks (local maxima)
    peaks, _ = find_peaks(ys, height=(peak_lims + dist_from_pl, np.amax(ys)), distance=dist,prominence = prom)
    # positions for negative peaks (local minima)
    antipeaks, _ = find_peaks(-ys, height=(-peak_lims + dist_from_pl, np.amax(-ys)), distance=dist,prominence = prom)

    return (peaks, antipeaks)

def get_pes_peaks(data, big_sigma = 300, small_sigma = 25, dist_from_pl = 0, dist = 1, prom = 0.07) -> list:
    """receives a list with a pes signal, and tries to find the local peaks just
    before the the cycles starts decending to its valley.
    Returns numpy array of x-axis positions of peaks in signal.
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
    peaks, _ = find_peaks(ys, height=(very_smoothed_sgnl + dist_from_pl, np.amax(ys)), distance=dist,prominence = prom)
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
            cnt+=1
            if cnt == v_c_len:
                break

    return pes_peaks


if __name__ == '__main__':
    # positions for positive peaks (local maxima)
    path = ".../../data/01_ PVE 1_Importacion de datos filtrados_con graficos.xlsm"
    edi, pes = read_file(path)
    get_signal_peaks(edi, 0, len(edi), 1.8, -1)
    # get_signal_peaks(pes, 23500, 25000, 1.8, -1)
