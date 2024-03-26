import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(0, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

p = GPIO.PWM(20, 1000)
p.start(0)

try:
    while True:
        x = int(input())
        p.ChangeDutyCycle(x)
        print(3.3*x/100)
finally:
    GPIO.cleanup()


