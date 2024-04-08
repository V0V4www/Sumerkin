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
    for value in range(256):
        signal = num2dac(value)
        time.sleep(0.0007)
        voltage = value / levels * maxVoltage
        comparatorValue = GPIO.input(comp)
        if comparatorValue == 1:
            print('ADC value = {:^3} -> {}, input voltage = {:.2f}'.format(value, signal, voltage))
            break


try:
    while True:
        adc()
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")