from dataclasses import dataclass

from RPi import GPIO
from pi_sht1x import SHT1x, SHT1xError

from mqtt import publish_message
from settings import TEMPERATURE_SENSOR_DATA_PIN, TEMPERATURE_SENSOR_SCK_PIN


@dataclass
class TemperatureMeasurement:
    temp_value: int
    humidity_value: int

    def save_to_mqtt(self):
        publish_message("temperature", self.temp_value)
        publish_message("humidity", self.humidity_value)


def get_temperature_data() -> TemperatureMeasurement:
    try:
        with SHT1x(TEMPERATURE_SENSOR_DATA_PIN, TEMPERATURE_SENSOR_SCK_PIN, otp_no_reload=True,
                   gpio_mode=GPIO.BCM) as sensor:
            temp = sensor.read_temperature()
            return TemperatureMeasurement(temp, sensor.read_humidity())
    except SHT1xError:
        # Using mock data instead of real if sensor is not connected
        return TemperatureMeasurement(20, 50)
