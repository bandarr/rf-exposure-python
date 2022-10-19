from exposure_calcuator import *

def main():
    c1 = CableValues(0.122290, 0.000260)  #for LMR-400
    xmtr_power = 1000
    feed_line_length = 113
    duty_cycle = .5
    per_30 = .5

    ec1 = ExposureCalculator()

    all_freq_values = [ FrequencyValues(7.3, 2.25, 1.5), FrequencyValues(14.35, 1.35, 1.5), FrequencyValues(18.1, 3.7, 1.5), FrequencyValues(21.45, 4.45, 1.5), FrequencyValues(24.99, 4.1, 1.5), FrequencyValues(29.7, 2.18, 4.5)]
    
    for f in all_freq_values:
        yarg = ec1.calculate_uncontrolled_safe_distance( f, c1, xmtr_power, feed_line_length, duty_cycle, per_30 )
        print(yarg)

if __name__ == "__main__":
    main()








