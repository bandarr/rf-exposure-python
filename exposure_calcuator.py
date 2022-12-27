from unicodedata import name

import math


class FrequencyValues:
    def __init__(self, freq: float, swr: float, gaindbi: float):
        self.freq = freq
        self.swr = swr
        self.gaindbi = gaindbi


class CableValues:
    def __init__(self, k1: float, k2: float):
        self.k1 = k1
        self.k2 = k2


class ExposureCalculator:

    def __calculate_reflection_coefficient(self, freq_values: FrequencyValues):
        return abs((freq_values.swr - 1)/(freq_values.swr + 1))

    def __calculate_feedline_loss_for_matched_load_at_frequency(self, feedline_length: int, feedline_loss_per_100ft_at_frequency: float) -> float:
        return (feedline_length/100) * feedline_loss_per_100ft_at_frequency

    def __calculate_feedline_loss_for_matched_load_at_frequency_percentage(self, feedline_loss_for_matched_load: float) -> float:
        return 10**(-feedline_loss_for_matched_load/10)

    def __calculate_feedline_loss_per_100ft_at_frequency(self, freq_values: FrequencyValues, cable_values: CableValues) -> float:
        return cable_values.k1 * math.sqrt(freq_values.freq + cable_values.k2 * freq_values.freq)

    def __calculate_feedline_loss_for_swr(self, feedline_loss_for_matched_load_percentage: float, gamma_squared: float) -> float:
        return -10 * math.log10(feedline_loss_for_matched_load_percentage * ((1 - gamma_squared)/(1 - feedline_loss_for_matched_load_percentage**2 * gamma_squared)))

    def __calculate_feedline_loss_for_swr_percentage(self, feedline_loss_for_swr: float) -> float:
        return (100 - 100/(10**(feedline_loss_for_swr/10)))/100

    def calculate_uncontrolled_safe_distance(self, freq_values: FrequencyValues, cable_values: CableValues, transmitter_power: int,
                                             feedline_length: int, duty_cycle: float, uncontrolled_percentage_30_minutes: float) -> float:

        gamma = self.__calculate_reflection_coefficient(freq_values)

        feedline_loss_per_100ft_at_frequency = self.__calculate_feedline_loss_per_100ft_at_frequency(
            freq_values, cable_values)

        feedline_loss_for_matched_load_at_frequency = self.__calculate_feedline_loss_for_matched_load_at_frequency(
            feedline_length, feedline_loss_per_100ft_at_frequency)

        feedline_loss_for_matched_load_at_frequency_percentage = self.__calculate_feedline_loss_for_matched_load_at_frequency_percentage(
            feedline_loss_for_matched_load_at_frequency)

        gamma_squared = abs(gamma)**2

        feedline_loss_for_swr = self.__calculate_feedline_loss_for_swr(
            feedline_loss_for_matched_load_at_frequency_percentage, gamma_squared)

        feedline_loss_for_swr_percentage = self.__calculate_feedline_loss_for_swr_percentage(
            feedline_loss_for_swr)

        power_loss_at_swr = feedline_loss_for_swr_percentage * transmitter_power

        peak_envelope_power_at_antenna = transmitter_power - power_loss_at_swr

        uncontrolled_average_pep = peak_envelope_power_at_antenna * \
            duty_cycle * uncontrolled_percentage_30_minutes

        mpe_s = 180/(freq_values.freq**2)

        gain_decimal = 10**(freq_values.gaindbi/10)

        # TODO:  Include effects of ground reflections

        return math.sqrt((0.219 * uncontrolled_average_pep * gain_decimal)/mpe_s)
