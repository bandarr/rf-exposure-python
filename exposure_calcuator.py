class FrequencyValues:
    def __init__(self, freq, swr, gaindbi):
        self.freq = freq
        self.swr = swr
        self.gaindbi = gaindbi


class ExposureCalculator:
    def calculate_uncontrolled_safe_distance( freq_values, xmtr_power, feedline_loss_100, feedline_length, duty_cycle, uncontrolled_percentage_30):
        