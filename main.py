from exposure_calcuator import *

def main():
    f1 = FrequencyValues(7.3, 2.25, 1.5)
    xmtr_power = 1000
    feed_line_length = 113
    loss_per_100 = 0.5
    duty_cycle = .5
    per_30 = .5

    ec1 = ExposureCalculator()

    yarg = ec1.calculate_uncontrolled_safe_distance( f1, xmtr_power, loss_per_100, feed_line_length, duty_cycle, per_30 )
    
    print(yarg)

if __name__ == "__main__":
    main()








