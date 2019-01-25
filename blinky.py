import RPi.GPIO as GPIO
import time

pin = 31
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

try:
    while True:

        GPIO.output(pin, GPIO.LOW)
        time.sleep(1)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)

finally:
    GPIO.cleanup()
    print("This code still ran")
