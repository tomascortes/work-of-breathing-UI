
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks
from data_processing.read_data import read_file


def get_signal_peaks(data, first_dp, last_dp, min_max, max_min, dist=150) -> tuple:
    """recives a list with a signal, and tries to find its inflection point,
    returning it as a tuple (xpos,ypos). Not finished
    """

    # xs corresponds to x coordinates and ys to the signal values
    xs, ys = np.arange(last_dp-first_dp), np.array(data[first_dp:last_dp])

    # Signal "energy"
    # yss = np.square(ys)

    # inverted signal
    ysi = -1*ys

    # smooth out noise
    # smoothed = gaussian_filter(ys, 3.)

    # inverted smoothed signal
    # smoothedi = -1*smoothed

    # positions for positive peaks (local maxima)
    peaks, _ = find_peaks(ys, height=min_max, distance=dist)
    # positions for negative peaks (local minima)
    antipeaks, _ = find_peaks(ysi, height=(max_min, 0), distance=dist)

    # positions for positive peaks (local maxima)
    # peaks, _ = find_peaks(smoothed, height = min_max, distance = dist)
    # positions for negative peaks (local minima)
    # antipeaks, _ = find_peaks(smoothedi, height = (max_min, 0), distance = dist)
    return (peaks, antipeaks)


if __name__ == '__main__':
    # positions for positive peaks (local maxima)
    path = ".../../data/01_ PVE 1_Importacion de datos filtrados_con graficos.xlsm"
    edi, pes = read_file(path)
    get_signal_peaks(edi, 0, len(edi), 1.8, -1)
    # get_signal_peaks(pes, 23500, 25000, 1.8, -1)
