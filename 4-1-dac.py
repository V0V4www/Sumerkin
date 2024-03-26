import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)


def decimal2binary(val):
    return [int(el) for el in bin(val)[2:].zfill(8)]


def assumed_voltage(val):
    return round((3.3 / 256) * val, 2)


try:
    while True:
        input_ = input('Please enter a number between 0 and 255:')
        if input_ == 'q':
            break
        elif input_.isalpha():
            print('Entered value is not a number')
        value = int(input_)
        if not input_.isnumeric() and not type(value) != "<class 'int'>":
            print('Entered value is not an integer')
        elif value < 0:
            print('Entered value is negative')
        elif value >= 256:
            print('Entered value is too large')
        bin_value = decimal2binary(value)
        
        for i in range(8):
            GPIO.output(dac[i], bin_value[i])
        
        print(bin_value)
        print(f'{assumed_voltage(value)} V')

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()

