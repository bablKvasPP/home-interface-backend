from dataclasses import dataclass
from pi_sht1x import SHT1x
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
    with SHT1x(TEMPERATURE_SENSOR_DATA_PIN, TEMPERATURE_SENSOR_SCK_PIN, otp_no_reload=True) as sensor:
        temp = sensor.read_temperature()
        return TemperatureMeasurement(temp, sensor.read_humidity())
