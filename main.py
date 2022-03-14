import sched
import time

from connections import connections
from hardware_components import hardware
from storage import storage
from temperature import get_temperature_data

connections.initialize()
hardware.initialize()
storage.load()
hardware.reinit()
s = sched.scheduler(time.time, time.sleep)


def save_data_to_mqtt(sc):
    temp_data = get_temperature_data()
    temp_data.save_to_mqtt()
    connections.logger.debug(f"Temp data saved to mqtt (t={temp_data.temp_value}º, h={temp_data.humidity_value}%)")
    hardware.reinit()
    s.enter(20, 1, save_data_to_mqtt, (sc,))


def alert_on_high(sc):
    temp_data = get_temperature_data()
    if temp_data.temp_value > storage.alert_threshold:
        hardware.buzzer.alert()
    else:
        hardware.buzzer.silence()


s.enter(20, 1, save_data_to_mqtt, (s,))
s.enter(5, 1, alert_on_high, (s,))
try:
    s.run()
except KeyboardInterrupt:
    connections.logger.error("Bye-Bye")
    connections.mqtt_client.loop_stop()
    hardware.stop()
    exit()
