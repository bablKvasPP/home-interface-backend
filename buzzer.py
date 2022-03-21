from time import sleep

from RPi import GPIO

from settings import BUZZER_PIN


class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.buzzer_pwm = GPIO.PWM(self.pin, 0.5)

    def alert(self):
        self.buzzer_pwm.start(50)

    def silence(self):
        self.buzzer_pwm.stop()


if __name__ == '__main__':
    from hardware_components import hardware
    hardware.initialize()
    hardware.buzzer.alert()
    sleep(1)
    hardware.buzzer.silence()
