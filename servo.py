from time import sleep

import RPi.GPIO as GPIO
from settings import SERVO_DOOR_PIN

class Servo:
    def __init__(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin
        self.servo_pwm = None

    def set_servo_angle(self, angle, hold=False):
        if not self.servo_pwm:
            self.servo_pwm = GPIO.PWM(self.pin, 50)

        self.servo_pwm.start(0)
        dutyCycle = angle / 20 + 3.
        self.servo_pwm.ChangeDutyCycle(dutyCycle)
        sleep(0.7)
        if not hold:
            self.servo_pwm.stop()
            self.servo_pwm = None


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    servo = Servo(SERVO_DOOR_PIN)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)
    while True:
        servo.set_servo_angle(0)
        sleep(0.5)
        servo.set_servo_angle(180)
        sleep(0.5)
