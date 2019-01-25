import time
import RPi.GPIO as GPIO
class Securitron:

    def initialize(self, robot_name="victor"):
        if not self:
            self = Securitron(robot_name)
            return self
        else:
            return self

    def __init__(self, robot_name="victor"):
        self.robot_name = robot_name
        GPIO.setmode(GPIO.BOARD)
        self.servo_pin = 32
        self.frequency_servo = 50
        self.heart_pin = 16
        self.enable_wheels = 33
        self.wheel_in_two = 29  # low
        self.wheel_in_one = 31  # high
        self.frequency = 500
        GPIO.setup(self.heart_pin, GPIO.OUT)
        GPIO.setup(self.enable_wheels, GPIO.OUT)
        GPIO.setup(self.wheel_in_one, GPIO.OUT)
        GPIO.setup(self.wheel_in_two, GPIO.OUT)
        GPIO.output(self.wheel_in_one, GPIO.HIGH)
        GPIO.output(self.wheel_in_two, GPIO.LOW)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm_wheel = GPIO.PWM(self.enable_wheels, self.frequency)
        self.pwm_servo = GPIO.PWM(self.servo_pin, self.frequency_servo)
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
        time.sleep(0.3)
        GPIO.output(self.heart_pin, GPIO.HIGH)
        time.sleep(0.3)

    def forward(self):
        print("Yes Sir! Going forward")
        GPIO.output(self.wheel_in_one, GPIO.LOW)
        GPIO.output(self.wheel_in_two, GPIO.HIGH)
        self.pwm_wheel.start(100)
        self.pwm_servo.start(7.5)
        # 7.5

    def forward_left(self):
        print("Yes Sir! Turning left")
        GPIO.output(self.wheel_in_one, GPIO.LOW)
        GPIO.output(self.wheel_in_two, GPIO.HIGH)
        self.pwm_wheel.start(60)
        self.pwm_servo.start(2.5)
        # 2.5

    def forward_right(self):
        print("Yes Sir! Turning right")
        GPIO.output(self.wheel_in_one, GPIO.LOW)
        GPIO.output(self.wheel_in_two, GPIO.HIGH)
        self.pwm_wheel.start(60)
        self.pwm_servo.start(12.5)
        # 12.5

    def back(self):
        print("Yes Sir! Going backwards")
        GPIO.output(self.wheel_in_one, GPIO.HIGH)
        GPIO.output(self.wheel_in_two, GPIO.LOW)
        self.pwm_wheel.start(100)
        self.pwm_servo.start(7.5)
        # 7.5

    def back_left(self):
        print("Yes Sir! Going backwards turning left")
        GPIO.output(self.wheel_in_one, GPIO.HIGH)
        GPIO.output(self.wheel_in_two, GPIO.LOW)
        self.pwm_wheel.start(60)
        self.pwm_servo.start(2.5)
        # 2.5

    def back_right(self):
        print("Yes Sir! Going backwards turning right")
        GPIO.output(self.wheel_in_one, GPIO.HIGH)
        GPIO.output(self.wheel_in_two, GPIO.LOW)
        self.pwm_wheel.start(60)
        self.pwm_servo.start(12.5)
        # 12.5

    def hit_breaks(self):
        print("Coming to a stop Sir!")
        GPIO.output(self.wheel_in_one, GPIO.LOW)
        GPIO.output(self.wheel_in_two, GPIO.LOW)
        self.pwm_wheel.stop()
        self.pwm_servo.start(7.5)
        # 7.5

    def go_home(self):
        self.hit_breaks()
        print("connection Close")
        GPIO.cleanup()
