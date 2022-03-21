import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import digitalio
from RPi import GPIO
from light_sensor import LightSensor

from buzzer import Buzzer
from led import RGBLed, LED
from settings import RGB_LED_R_PIN, RGB_LED_B_PIN, RGB_LED_G_PIN, HEATER_LED_INDICATOR_PIN, BUZZER_PIN
from storage import storage


class HardwareComponents:
    rgb_led: RGBLed
    heater: LED
    buzzer: Buzzer
    spi: SPI
    cs: digitalio.DigitalInOut
    mcp: Adafruit_MCP3008.MCP3008
    light_sensor: LightSensor

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        self.rgb_led = RGBLed(RGB_LED_R_PIN, RGB_LED_G_PIN, RGB_LED_B_PIN)
        self.heater = LED(HEATER_LED_INDICATOR_PIN)
        self.buzzer = Buzzer(BUZZER_PIN)
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))
        self.light_sensor = LightSensor(0)

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
