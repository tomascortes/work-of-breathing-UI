from src.backend.peak_finder.signal_processing import get_edi_peaks, get_pes_peaks
from params import MAX_INTEGRAL_VALUE

class Integration:
    def __init__(self, data_edi, data_pes):

        self.data_edi = data_edi
        self.data_pes = data_pes
        # self.small_sigma_edi = 25
        self.big_sigma_edi = 300
        self.small_sigma_edi = 25
        self.big_sigma_pes = 300
        self.small_sigma_pes = 25


    def points_75_percent(self) -> list:
        '''
        returns the list of the index of all points 
        where the decreasing edi curve reaches the 75%
        of the amplitude
        '''
        indexes_75 = []
        peaks, antipeaks, _ = get_edi_peaks(
            self.data_edi, 
            big_sigma=self.big_sigma_pes,
            small_sigma = self.small_sigma_pes)
        peak_index = 0

        # the start of the cicle is antipeak
        while self.data_edi[peaks[peak_index]] < self.data_edi[antipeaks[0]]:
            peak_index += 1

        for anti_p_index in antipeaks:
            min_v = self.data_edi[anti_p_index]
            max_v = self.data_edi[peaks[peak_index]]
            amplitude = max_v - min_v
            for index_75 in range(peaks[peak_index], anti_p_index + 1):
                if self.data_edi[index_75] <= amplitude*0.7:
                    indexes_75.append(index_75)
                    peak_index += 1
                    break

        return indexes_75

    def integration_pes(self) -> list:
        '''
        Return list of lists where each list
        contains
        [integral_value on pes, start_integral, end_integral]
        '''
        integral_values = []
        dx = 1/100

        index_peaks_pes, _, _ = get_pes_peaks(self.data_pes,
                                              big_sigma=self.big_sigma_pes,
                                              small_sigma=self.small_sigma_pes)
        index_75 = self.points_75_percent()


        for start_pointer in range(len(index_peaks_pes) - 1):
            max_value = self.data_pes[index_peaks_pes[start_pointer]]
            s = 0
            end_pointer = self.next_75_value(
                start_pointer, index_peaks_pes, index_75)
            if not end_pointer:
                continue

            len_cicle = len(self.data_pes[index_peaks_pes[start_pointer]:index_75[end_pointer]])
            s = sum(self.data_pes[index_peaks_pes[start_pointer]:index_75[end_pointer]])
            s = max_value*len_cicle - s
            s *= dx
            if MAX_INTEGRAL_VALUE < s:
                continue
            # store the values with the corresponding ones used to calculate them
            integral_values.append(
                [s, index_peaks_pes[start_pointer], index_75[end_pointer]])

        # If there are repeated ends of integral, we keep just the last one
        count = 0
        while count < len(integral_values) -1:
            if integral_values[count][2] == integral_values[count + 1][2]:
                integral_values.pop(count)
            else:
                count += 1

        return integral_values


    def integration_edi(self) -> list:
        integral_values = []
        dx = 1/100

        _, index_anti_peaks, _ = get_edi_peaks(self.data_edi,
                                              big_sigma=self.big_sigma_edi)
        index_75 = self.points_75_percent()


        for start_pointer in range(len(index_anti_peaks) - 1):
            min_value = self.data_edi[index_anti_peaks[start_pointer]]
            s = 0
            end_pointer = self.next_75_value(
                start_pointer, index_anti_peaks, index_75)
            if not end_pointer:
                continue

            len_cicle = len(self.data_edi[index_anti_peaks[start_pointer]:index_75[end_pointer]])
            # First we sum all the values from 0 to the edi curve
            s = sum(self.data_edi[index_anti_peaks[start_pointer]:index_75[end_pointer]])
            # Then we rest the rectangle corresponding to the min value
            s = s- min_value*len_cicle
            # to optimize the process we multiply at the end for the dx
            s *= dx
            if MAX_INTEGRAL_VALUE < s:
                continue
            # store the values with the corresponding ones used to calculate them
            integral_values.append(
                [s, index_anti_peaks[start_pointer], index_75[end_pointer]])

        # If there are repeated ends of integral, we keep just the last one
        count = 0
        while count < len(integral_values) -1:
            if integral_values[count][2] == integral_values[count + 1][2]:
                integral_values.pop(count)
            else:
                count += 1

        return integral_values

    def next_75_value(self, start_pointer, index_peaks, index_75) -> int:
        '''
        Recives int used as pointer start_pointer, the list of index_peaks and
        teh list of index_75 and return the pointer corresponding to the next 
        index_75 value'''

        for i in range(len(index_75)):
            if index_75[i] > index_peaks[start_pointer]:
                return i