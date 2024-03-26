import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)
GPIO.output(dac, 0)


def decimal2binary(val):
    return [int(el) for el in bin(val)[2:].zfill(8)]


def assumed_voltage(val):
    return round((3.3 / 256) * val, 2)


try:
    period = 1
    t = period / 512
    while True:
        for i in range(256):
            binary = decimal2binary(i)
            for k in range(8):
                GPIO.output(dac[k], binary[k])
            time.sleep(t)
            GPIO.output(dac, 0)
        for l in range(256):
            binary = decimal2binary(255 - l)
            for j in range(8):
                GPIO.output(dac[j], binary[j])
            time.sleep(t)
            GPIO.output(dac, 0)
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()