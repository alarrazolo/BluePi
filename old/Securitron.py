import time
import RPi.GPIO as GPIO
class Securitron:

    def __init__(self, robot_name="victor"):
        self.robot_name = robot_name
        try:
            GPIO.cleanup()
        except RuntimeWarning:
            pass
        GPIO.setmode(GPIO.BOARD)
        self.heart_pin = 16
        # self.right_side_wheels = 32
        # self.right_side_in_one = 11  # low
        # self.right_side_in_two = 13  # high
        # self.left_side_wheels = 33
        # self.left_side_in_two = 29  # low
        # self.left_side_in_one = 31  # high
        self.enable_wheels = 33
        self.wheel_in_two = 29  # low
        self.wheel_in_one = 31  # high
        self.frequency = 500
        GPIO.setup(self.heart_pin, GPIO.OUT)
        # GPIO.setup(self.right_side_wheels, GPIO.OUT)
        GPIO.setup(self.enable_wheels, GPIO.OUT)
        # GPIO.setup(self.right_side_in_one, GPIO.OUT)
        # GPIO.setup(self.right_side_in_two, GPIO.OUT)
        GPIO.setup(self.wheel_in_one, GPIO.OUT)
        GPIO.setup(self.wheel_in_two, GPIO.OUT)
        # GPIO.output(self.right_side_in_one, GPIO.LOW)
        # GPIO.output(self.right_side_in_two, GPIO.HIGH)
        GPIO.output(self.wheel_in_one, GPIO.HIGH)
        GPIO.output(self.wheel_in_two, GPIO.LOW)
        # self.pwm_right = GPIO.PWM(self.right_side_wheels, self.frequency)
        self.pwm_wheel = GPIO.PWM(self.enable_wheels, self.frequency)
        self.enable_flag = True


    @property
    def robot_name(self):
        return self._robot_name

    @robot_name.setter
    def robot_name(self, name):
        if not isinstance(name, str):
            print("Expected a string!")
        else:
            self._robot_name = name

    @robot_name.deleter
    def robot_name(self):
        print("name cannot be deleted")

    def beat_heart(self):
        GPIO.output(self.heart_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.heart_pin, GPIO.HIGH)
        time.sleep(0.1)

    def forward(self):
        print("Yes Sir! Going forward")
        # GPIO.output(self.right_side_in_one, GPIO.HIGH)
        # GPIO.output(self.right_side_in_two, GPIO.LOW)
        GPIO.output(self.wheel_in_one, GPIO.LOW)
        GPIO.output(self.wheel_in_two, GPIO.HIGH)
        # self.pwm_right.start(80)
        self.pwm_wheel.start(100)

    def forward_left(self):
        print("Yes Sir! Turning left")
        # GPIO.output(self.right_side_in_one, GPIO.HIGH)
        # GPIO.output(self.right_side_in_two, GPIO.LOW)
        GPIO.output(self.wheel_in_one, GPIO.LOW)
        GPIO.output(self.wheel_in_two, GPIO.HIGH)
        # self.pwm_right.start(90)
        self.pwm_wheel.start(60)

    def forward_right(self):
        print("Yes Sir! Turning right")
        # GPIO.output(self.right_side_in_one, GPIO.HIGH)
        # GPIO.output(self.right_side_in_two, GPIO.LOW)
        GPIO.output(self.wheel_in_one, GPIO.LOW)
        GPIO.output(self.wheel_in_two, GPIO.HIGH)
        # self.pwm_right.start(30)
        self.pwm_wheel.start(60)

    # def strong_left(self):
    #     print("Yes Sir! Turning left in place")
    #     GPIO.output(self.right_side_in_one, GPIO.LOW)
    #     GPIO.output(self.right_side_in_two, GPIO.HIGH)
    #     GPIO.output(self.left_side_in_one, GPIO.LOW)
    #     GPIO.output(self.left_side_in_two, GPIO.HIGH)
    #     self.pwm_right.start(80)
    #     self.pwm_left.start(80)
    #
    # def strong_right(self):
    #     print("Yes Sir! Turning right in place")
    #     GPIO.output(self.right_side_in_one, GPIO.HIGH)
    #     GPIO.output(self.right_side_in_two, GPIO.LOW)
    #     GPIO.output(self.left_side_in_one, GPIO.HIGH)
    #     GPIO.output(self.left_side_in_two, GPIO.LOW)
    #     self.pwm_right.start(80)
    #     self.pwm_left.start(80)

    def back(self):
        print("Yes Sir! Going backwards")
        # GPIO.output(self.right_side_in_one, GPIO.LOW)
        # GPIO.output(self.right_side_in_two, GPIO.HIGH)
        GPIO.output(self.wheel_in_one, GPIO.HIGH)
        GPIO.output(self.wheel_in_two, GPIO.LOW)
        # self.pwm_right.start(80)
        self.pwm_wheel.start(100)

    def back_left(self):
        print("Yes Sir! Going backwards turning left")
        # GPIO.output(self.right_side_in_one, GPIO.LOW)
        # GPIO.output(self.right_side_in_two, GPIO.HIGH)
        GPIO.output(self.wheel_in_one, GPIO.HIGH)
        GPIO.output(self.wheel_in_two, GPIO.LOW)
        # self.pwm_right.start(90)
        self.pwm_wheel.start(60)

    def back_right(self):
        print("Yes Sir! Going backwards turning right")
        # GPIO.output(self.right_side_in_one, GPIO.LOW)
        # GPIO.output(self.right_side_in_two, GPIO.HIGH)
        GPIO.output(self.wheel_in_one, GPIO.HIGH)
        GPIO.output(self.wheel_in_two, GPIO.LOW)
        # self.pwm_right.start(30)
        self.pwm_wheel.start(60)

    def hit_breaks(self):
        print("Coming to a stop Sir!")
        # GPIO.output(self.right_side_in_one, GPIO.LOW)
        # GPIO.output(self.right_side_in_two, GPIO.LOW)
        GPIO.output(self.wheel_in_one, GPIO.LOW)
        GPIO.output(self.wheel_in_two, GPIO.LOW)
        # self.pwm_right.stop()
        self.pwm_wheel.stop()

    def go_home(self):
        GPIO.cleanup()
