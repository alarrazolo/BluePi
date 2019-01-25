import time
import RPi.GPIO as GPIO


def main():
    try:
        GPIO.setmode(GPIO.BOARD)
        servo_pin = 32
        frequency_servo = 50
        GPIO.setup(servo_pin, GPIO.OUT)
        pwm_servo = GPIO.PWM(servo_pin, frequency_servo)
        pwm_servo.start(7.5)
        time.sleep(2)
        pwm_servo.start(2.5)
        time.sleep(2)
        pwm_servo.start(12.5)
        time.sleep(2)
        pwm_servo.start(7.5)
        time.sleep(2)
        pwm_servo.stop()
        GPIO.cleanup()
        print("Code ran successfully")
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Code ran successfully")

    # try:
    #     while True:
    #         GPIO.output(servo_pin, GPIO.LOW)
    #         time.sleep(.01)
    #         GPIO.output(servo_pin, GPIO.HIGH)
    #         time.sleep(.01)
    # except KeyboardInterrupt:
    #     print("Code ran successfully")

if __name__ == "__main__":
    main()
