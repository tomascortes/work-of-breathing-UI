
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks
from data_processing.read_data import read_file


def get_signal_peaks(path, first_dp, last_dp, min_max, max_min, dist = 150):
    """recives a list with a signal, and tries to find its inflection point,
    returning it as a tuple (xpos,ypos). Not finished
    """
    signals = read_file(path)

    # xs corresponds to x coordinates and ys to the signal values
    xs, ys = np.arange(last_dp-first_dp), np.array(signals[0][first_dp:last_dp])

    # Signal "energy"
    # yss = np.square(ys)

    #inverted signal
    ysi = -1*ys

    # smooth out noise
    # smoothed = gaussian_filter(ys, 3.)

    #inverted smoothed signal
    # smoothedi = -1*smoothed

    # positions for positive peaks (local maxima)
    peaks, _ = find_peaks(ys, height = min_max, distance = dist)
    # positions for negative peaks (local minima)
    antipeaks, _ = find_peaks(ysi, height = (max_min, 0), distance = dist)

    # positions for positive peaks (local maxima)
    # peaks, _ = find_peaks(smoothed, height = min_max, distance = dist)
    # positions for negative peaks (local minima)
    # antipeaks, _ = find_peaks(smoothedi, height = (max_min, 0), distance = dist)

    # plot datapoints
    plt.plot(xs, ys, '.')
    # plt.plot(xs, smoothed, '-')
    # plt.plot(xs, smoothedi, '-')
    plt.plot(peaks, ys[peaks], "x")
    # plt.plot(peaks, smoothed[peaks], "x")
    plt.plot(antipeaks, ys[antipeaks], "x")
    # plt.plot(antipeaks, smoothed[antipeaks], "x")
    # plot min local max and max local min thresholds
    plt.plot(np.full(last_dp-first_dp, min_max), "--", color="gray")
    plt.plot(np.full(last_dp-first_dp, max_min), "--", color="gray")

    # first and second derivatives of our signal
    # fstgradient = np.gradient(smoothed, np.arange(smoothed.size))
    # plt.plot(xs, np.gradient(fstgradient, np.arange(fstgradient.size)))

    # Plot energy
    # plt.plot(xs,yss)
    # plt.plot(x0, y0, 'o')
    plt.show()


if __name__ == '__main__':
    # positions for positive peaks (local maxima)
    get_signal_peaks("../data/01_ PVE 1_Importacion de datos filtrados_con graficos.xlsm", 23500, 25000, 1.8, -1)