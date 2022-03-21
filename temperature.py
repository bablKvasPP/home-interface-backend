from dataclasses import dataclass
from datetime import datetime

from RPi import GPIO
from pi_sht1x import SHT1x, SHT1xError

from mqtt import publish_message
from settings import TEMPERATURE_SENSOR_DATA_PIN, TEMPERATURE_SENSOR_SCK_PIN

global previous_measurement_time
previous_measurement_time = 0
global previous_measurement
previous_measurement = None


@dataclass
class TemperatureMeasurement:
    temp_value: int
    humidity_value: int

    def save_to_mqtt(self):
        publish_message("temperature", self.temp_value)
        publish_message("humidity", self.humidity_value)


def get_temperature_data() -> TemperatureMeasurement:
    # because of sensor timeout there is some builtin timeout, based on previous measurement
    global previous_measurement_time
    global previous_measurement
    if datetime.now().timestamp() - previous_measurement_time > 20:
        try:
            with SHT1x(TEMPERATURE_SENSOR_DATA_PIN, TEMPERATURE_SENSOR_SCK_PIN, otp_no_reload=True,
                       gpio_mode=GPIO.BCM) as sensor:
                temp = sensor.read_temperature()
                previous_measurement_time = datetime.now().timestamp()
                measurement = TemperatureMeasurement(temp, sensor.read_humidity())
                previous_measurement = measurement
                return measurement
        except SHT1xError:
            # Using mock data instead of real if sensor is not connected
            return TemperatureMeasurement(30, 50)
    else:
        return previous_measurement
