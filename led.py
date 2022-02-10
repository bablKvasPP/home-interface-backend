import RPi.GPIO as GPIO

from storage import storage


class RGBLed:
    """ Some not so good code here """

    def __init__(self, r_pin, g_pin, b_pin):
        self.r_pin = r_pin
        self.g_pin = g_pin
        self.b_pin = b_pin
        self.setup_pinout()
        self.r_pwm = GPIO.PWM(self.r_pin, 100)
        self.g_pwm = GPIO.PWM(self.g_pin, 100)
        self.b_pwm = GPIO.PWM(self.b_pin, 100)
        self.start_pwm()

    def start_pwm(self):
        self.r_pwm.start(0)
        self.g_pwm.start(0)
        self.b_pwm.start(0)

    def stop_pwm(self):
        self.r_pwm.stop(0)
        self.g_pwm.stop(0)
        self.b_pwm.stop(0)

    def setup_pinout(self):
        GPIO.setup(self.r_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.g_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.b_pin, GPIO.OUT, initial=GPIO.LOW)

    def set_rgb(self, r=None, g=None, b=None):
        multiply_koef = 1 / 2.55
        if r is not None:
            self.r_pwm.ChangeDutyCycle(r * multiply_koef)
            storage.lights_r = r
        if g is not None:
            self.g_pwm.ChangeDutyCycle(g * multiply_koef)
            storage.lights_g = g
        if b is not None:
            self.b_pwm.ChangeDutyCycle(b * multiply_koef)
            storage.lights_b = b
        storage.save()


class LED:
    def __init__(self, pin):
        self.pin = pin
        self._state = 0
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def on(self):
        self.state = 1

    def off(self):
        self.state = 0

    def switch(self):
        self.state = int(not bool(self.state))

    @property
    def state(self):
        return self._state

    @state.setter
    def setter(self, value):
        self._state = value
        GPIO.output(self.pin, value)
