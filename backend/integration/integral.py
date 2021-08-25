from backend.peak_finder.signal_processing import get_edi_peaks, get_pes_peaks


class Integration:
    def __init__(self, data_edi, data_pes):

        self.data_edi = data_edi
        self.data_pes = data_pes
        # self.small_sigma_edi = 25
        self.small_sigma_pes = 25
        self.big_sigma_edi = 300
        self.big_sigma_pes = 300

    def points_70_percent(self) -> list:
        '''
        returns the list of the index of all points 
        where the decreasing edi curve reaches the 70%
        of the amplitude
        '''
        indexes_70 = []
        peaks, antipeaks, _ = get_edi_peaks(
            self.data_edi, big_sigma=self.big_sigma_pes)
        peak_index = 0

        # the start of the cicle is antipeak
        while self.data_edi[peaks[peak_index]] < self.data_edi[antipeaks[0]]:
            peak_index += 1

        for anti_p_index in antipeaks:
            min_v = self.data_edi[anti_p_index]
            max_v = self.data_edi[peaks[peak_index]]
            amplitude = max_v - min_v
            for index_70 in range(peaks[peak_index], anti_p_index + 1):
                if self.data_edi[index_70] <= amplitude*0.7:
                    indexes_70.append(index_70)
                    peak_index += 1
                    break

        return indexes_70

    def integration(self) -> list:
        '''
        Return list of lists where each list
        contains
        [integral_value, start_integral, end_integral]
        '''
        integral_values = []
        dx = 100

        index_peaks_pes, _, _ = get_pes_peaks(self.data_pes,
                                              big_sigma=self.big_sigma_pes,
                                              small_sigma=self.small_sigma_pes)
        index_70 = self.points_70_percent()

        for start_pointer in range(len(index_peaks_pes) - 1):
            max_value = self.data_pes[index_peaks_pes[start_pointer]]
            s = 0
            end_pointer = self.next_pes_int_stop(
                start_pointer, index_peaks_pes, index_70)
            if not end_pointer:
                continue
            for x in range(index_peaks_pes[start_pointer], index_70[end_pointer]):
                s += (max_value - self.data_pes[x])*dx

            # store the values with the corresponding ones used to calculate them
            integral_values.append(
                [s, index_peaks_pes[start_pointer], index_70[end_pointer]])
        return integral_values

    def next_pes_int_stop(self, start_pointer, index_peaks_pes, index_70) -> int:
        '''
        Recives int used as pointer start_pointer, the list of index_peaks_pes and
        teh list of index_70 and return the pointer corresponding to the next 
        index_70 value'''

        for i in range(len(index_70)):
            if index_70[i] > index_peaks_pes[start_pointer]:
                return i
