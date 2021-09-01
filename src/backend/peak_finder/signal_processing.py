
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


if __name__ == '__main__':
    # positions for positive peaks (local maxima)
    path = ".../../data/01_ PVE 1_Importacion de datos filtrados_con graficos.xlsm"
    edi, pes = read_file(path)
