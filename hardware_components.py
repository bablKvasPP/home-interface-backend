from time import sleep

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import digitalio
from RPi import GPIO
from light_sensor import LightSensor

from buzzer import Buzzer
from led import RGBLed, LED
from settings import RGB_LED_R_PIN, RGB_LED_B_PIN, RGB_LED_G_PIN, HEATER_LED_INDICATOR_PIN, BUZZER_PIN, COOLER_RELAY_PIN, SUCCESS_LED_PIN, FAIL_LED_PIN, CHECKING_LED_PIN, TICK_LED_PIN
from storage import storage


class HardwareComponents:
    rgb_led: RGBLed
    heater: LED
    cooler: LED
    buzzer: Buzzer
    spi: SPI
    cs: digitalio.DigitalInOut
    mcp: Adafruit_MCP3008.MCP3008
    light_sensor: LightSensor
    success_led: LED
    failed_led: LED
    tick_led: LED
    checking_led: LED

    def initialize(self):
        from connections import connections
        GPIO.setmode(GPIO.BCM)
        connections.logger.debug("Initializing hardware components")
        self.rgb_led = RGBLed(RGB_LED_R_PIN, RGB_LED_G_PIN, RGB_LED_B_PIN)
        self.heater = LED(HEATER_LED_INDICATOR_PIN)
        self.success_led = LED(SUCCESS_LED_PIN)
        self.failed_led = LED(FAIL_LED_PIN)
        self.tick_led = LED(TICK_LED_PIN)
        self.checking_led = LED(CHECKING_LED_PIN)
        self.buzzer = Buzzer(BUZZER_PIN)
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))
        self.light_sensor = LightSensor(0)
        self.cooler = LED(COOLER_RELAY_PIN, is_reversed=True)
        self.failed_led.on()
        sleep(0.2)
        self.checking_led.on()
        sleep(0.2)
        self.success_led.on()
        sleep(0.2)
        self.tick_led.on()
        sleep(0.2)
        self.checking_led.off()
        self.success_led.off()
        self.tick_led.off()
        connections.logger.debug("HardwareComponents intialized successful")

    def reinit(self):
        from connections import connections
        GPIO.setmode(GPIO.BCM)
        self.rgb_led.setup_pinout()
        self.rgb_led.start_pwm()
        self.rgb_led.set_rgb(storage.lights_r, storage.lights_g, storage.lights_b)

    def stop(self):
        self.rgb_led.stop_pwm()


global hardware
hardware = HardwareComponents()
