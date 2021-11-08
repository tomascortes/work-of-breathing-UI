from src.backend.peak_finder.signal_processing import get_edi_peaks_old
from src.backend.params import MAX_INTEGRAL_VALUE, MAX_INTEGRAL_VALUE_PES

class Integration:
    def __init__(self, data_edi, data_pes, signal_processor_edi, signal_processor_pes):

        self.data_edi = data_edi
        self.data_pes = data_pes
        self.big_sigma_edi = 300
        self.small_sigma_edi = 25
        self.big_sigma_pes = 300
        self.small_sigma_pes = 25
        self.old_edi_method = False

        self.sp_edi = signal_processor_edi
        self.sp_pes = signal_processor_pes

    def points_75_percent(self) -> list:
        '''
        returns the list of the index of all points 
        where the decreasing edi curve reaches the 75%
        of the amplitude
        '''
        indexes_75 = []
        if self.old_edi_method:
            peaks, antipeaks, _ = get_edi_peaks_old(
                self.data_edi, 
                big_sigma=self.big_sigma_pes)
        else:
            self.sp_edi.update_peaks(
                big_sigma=self.big_sigma_edi,
                small_sigma = self.small_sigma_edi)
            peaks = self.sp_edi.get_straight_signal_peaks()
            antipeaks = self.sp_edi.right_antipeaks

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
        [integral_value on pes, start_integral, end_integral, amplitud of cycle]
        '''
        integral_values = []
        dx = 1/100

        self.sp_pes.update_peaks(
            big_sigma=self.big_sigma_pes,
            small_sigma=self.small_sigma_pes)

        index_peaks_pes = self.sp_pes.right_peaks

        index_75 = self.points_75_percent()


        for start_pointer in range(len(index_peaks_pes) - 1):
            max_value = self.data_pes[index_peaks_pes[start_pointer]]
            s = 0
            end_pointer = self.next_75_value(
                start_pointer, index_peaks_pes, index_75)
            if not end_pointer:
                continue
            min_value = min(self.data_pes[index_peaks_pes[start_pointer]:index_75[end_pointer]])

            len_cicle = len(self.data_pes[index_peaks_pes[start_pointer]:index_75[end_pointer]])
            
            
            #Inferior Area
            s = sum(self.data_pes[index_peaks_pes[start_pointer]:index_75[end_pointer]])
            #superior Area minus the inferior area
            s = max_value*len_cicle - s
            #giving result in seconds
            s *= dx
            amplitude = max_value - min_value

            if MAX_INTEGRAL_VALUE < s:
                continue
            # store the values with the corresponding ones used to calculate them
            integral_values.append(
                [s, index_peaks_pes[start_pointer], index_75[end_pointer], amplitude])

        # If there are repeated ends of integral, we keep just the last one
        count = 0
        while count < len(integral_values) -1:
            if integral_values[count][2] == integral_values[count + 1][2]:
                integral_values.pop(count)
            else:
                count += 1

        return integral_values


    def integration_edi(self) -> list:
        '''
        Return list of lists where each list
        contains
        [integral_value on edu, start_integral, end_integral, amplitud of cycle]
        '''
        integral_values = []
        dx = 1/100
        if self.old_edi_method:
            _, index_anti_peaks, _ = get_edi_peaks_old(
                self.data_edi, 
                big_sigma=self.big_sigma_edi)
        else:
            self.sp_edi.update_peaks(
                big_sigma=self.big_sigma_edi,
                small_sigma = self.small_sigma_edi)

            index_anti_peaks = self.sp_edi.right_antipeaks

        index_75 = self.points_75_percent()


        for start_pointer in range(len(index_anti_peaks) - 1):
            min_value = self.data_edi[index_anti_peaks[start_pointer]]
            s = 0
            end_pointer = self.next_75_value(
                start_pointer, index_anti_peaks, index_75)
            if not end_pointer:
                continue
            max_value = max(self.data_edi[index_anti_peaks[start_pointer]:index_75[end_pointer]])

            len_cicle = len(self.data_edi[index_anti_peaks[start_pointer]:index_75[end_pointer]])
            # First we sum all the values from 0 to the edi curve
            s = sum(self.data_edi[index_anti_peaks[start_pointer]:index_75[end_pointer]])
            # Then we rest the rectangle corresponding to the min value
            s = s- min_value*len_cicle
            # to optimize the process we multiply at the end for the dx
            s *= dx
            if MAX_INTEGRAL_VALUE < s:
                continue
            amplitude = max_value - min_value
            # store the values with the corresponding ones used to calculate them
            integral_values.append(
                [s, index_anti_peaks[start_pointer], index_75[end_pointer], amplitude])

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
        index_75 value
        '''

        for i in range(len(index_75)):
            if index_75[i] > index_peaks[start_pointer]:
                return i

    def coordinated_integrals(self):
        integ_edi = self.integration_edi()
        integ_pes = self.integration_pes()
        count = 0
        

        while count < len(integ_edi) - 1 and count < len(integ_pes) -1 :
            if integ_edi[count][2] == integ_pes[count][2]:
                count += 1
            elif integ_edi[count][2] < integ_pes[count][2]:
                integ_edi.pop(count)
            elif integ_edi[count][2] > integ_pes[count][2]:
                integ_pes.pop(count)
        
        # it means the last one of one of the lists it isnt in the other one
        while len(integ_edi) != len(integ_pes):
            if  len(integ_edi) < len(integ_pes):
                integ_pes.pop()
            else:
                integ_edi.pop()

        return integ_edi, integ_pes

    def integration_pes_without_edi(self) -> list:
        '''
        Return list of lists where each list
        contains
        [integral_value on pes, start_integral, end_integral, amplitud of cycle]
        '''
        integral_values = []
        dx = 1/100

        self.sp_pes.update_peaks(
            big_sigma=self.big_sigma_pes,
            small_sigma = self.small_sigma_pes)

        index_peaks_pes = self.sp_pes.right_peaks
        


        for start_cicle in range(len(index_peaks_pes) - 1):
            max_value = self.data_pes[index_peaks_pes[start_cicle]]
            s = 0
            
            start_pointer = index_peaks_pes[start_cicle]
            end_pointer = self.next_25_point(
                start_pointer, 
                index_peaks_pes[start_cicle +1])

            if not end_pointer or end_pointer < start_pointer:
                continue
            min_value = min(self.data_pes[start_pointer:end_pointer])

            len_cicle = len(self.data_pes[start_pointer:end_pointer])
            #Inferior Area
            s = sum(self.data_pes[start_pointer:end_pointer])
            #superior Area minus the inferior area
            s = max_value*len_cicle - s
            #giving result in seconds
            s *= dx
            amplitude = max_value - min_value
            if MAX_INTEGRAL_VALUE_PES < s:
                continue
            # store the values with the corresponding ones used to calculate them
            integral_values.append(
                [s, start_pointer, end_pointer, amplitude])

        # If there are repeated ends of integral, we keep just the last one
        count = 0
        while count < len(integral_values) -1:
            if integral_values[count][2] == integral_values[count + 1][2]:
                integral_values.pop(count)
            else:
                count += 1

        return integral_values


    def next_25_point(self, start_x_val,  next_cicle):
        index_left_peaks_pes = self.sp_pes.left_peaks
        index_antipeaks_pes = self.sp_pes.get_straight_signal_peaks(True)
        next_left_p = self.next_betwen(start_x_val, next_cicle, index_left_peaks_pes)
        next_left_antp = self.next_betwen(start_x_val, next_cicle, index_antipeaks_pes)
        return round( 25 * (next_left_p - next_left_antp)/100 + next_left_antp)
        
    def next_betwen(self,start,end,list):
        for index in range(len(list)):
            if list[index] > start:
                return list[index]
            if end < list[index]:
                return end


                 
