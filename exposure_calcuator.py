from unicodedata import name

import math


class FrequencyValues:
    def __init__(self, freq, swr, gaindbi):
        self.freq = freq
        self.swr = swr
        self.gaindbi = gaindbi

class ExposureCalculator:
    
    def __calculate_reflection_coefficient(  self, freq_values ):
        return abs( (freq_values.swr - 1)/(freq_values.swr + 1) )

    def __get_matched_load_fraction(self, feedline_length, feedline_loss_100):
        feedline_loss_for_matched_load = (feedline_length/100) * feedline_loss_100
        return 10**((-feedline_loss_for_matched_load )/10)



    def calculate_uncontrolled_safe_distance( self, freq_values, xmtr_power, feedline_loss_100, feedline_length, duty_cycle, uncontrolled_percentage_30):
        gamma = self.__calculate_reflection_coefficient( freq_values )
        
        matched_load_fraction = self.__get_matched_load_fraction( feedline_length, feedline_loss_100 )

        gamma_squared = abs(gamma)**2

        one_minus_gamma_squared = 1 - gamma_squared

        denominator = 1 - (matched_load_fraction**2) * gamma_squared

        feed_line_loss = -10 * math.log10( matched_load_fraction * (one_minus_gamma_squared/denominator) )

        loss_percentage = (100 - 100/(10**(feed_line_loss/10)))/100

        power_loss = loss_percentage * xmtr_power

        pep_at_antenna = xmtr_power - power_loss

        uncontrolled_average_pep = pep_at_antenna * duty_cycle * uncontrolled_percentage_30

        mpe_s = 180/(freq_values.freq**2)

        gain_decimal = 10**(freq_values.gaindbi/10)

        uncontrolled_safe_distance = math.sqrt((0.219*uncontrolled_average_pep * gain_decimal)/mpe_s)

        return uncontrolled_safe_distance



    
        
