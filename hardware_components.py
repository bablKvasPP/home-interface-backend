from RPi import GPIO

from led import RGBLed, LED
from settings import RGB_LED_R_PIN, RGB_LED_B_PIN, RGB_LED_G_PIN, HEATER_LED_INDICATOR_PIN
from storage import storage


class HardwareComponents:
    rgb_led: RGBLed
    heater: LED

    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        self.rgb_led = RGBLed(RGB_LED_R_PIN, RGB_LED_G_PIN, RGB_LED_B_PIN)
        self.heater = LED(HEATER_LED_INDICATOR_PIN)

    def reinit(self):
        GPIO.setmode(GPIO.BOARD)
        self.rgb_led.setup_pinout()
        self.rgb_led.start_pwm()
        self.rgb_led.set_rgb(storage.lights_r, storage.lights_g, storage.lights_b)


global hardware
hardware = HardwareComponents()
