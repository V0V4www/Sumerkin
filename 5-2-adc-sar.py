import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
levels = 2**8
maxVoltage = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.output(dac, 0)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)


def decimal2binary(val):
    return [int(el) for el in bin(val)[2:].zfill(8)]


def num2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal


def adc():
    signal = [0] * 8
    for i in range(8):
        signal[i] = 1
        GPIO.output(dac, signal)
        time.sleep(0.0007)
        value = int(''.join([str(i) for i in signal]), 2)
        voltage = value / levels * maxVoltage
        comparatorValue = GPIO.input(comp)
        if comparatorValue == 1:
            signal[i] = 0
    True_value = int(''.join([str(i) for i in signal]), 2)
    True_voltage = True_value / levels * maxVoltage
    return True_voltage


try:
    while True:
        print(adc())
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")