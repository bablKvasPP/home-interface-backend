import sched
import time

from connections import connections
from hardware_components import hardware
from storage import storage
from temperature import get_temperature_data

connections.initialize()
hardware.initialize()
storage.load()
s = sched.scheduler(time.time, time.sleep)


def save_data_to_mqtt(sc):
    temp_data = get_temperature_data()
    temp_data.save_to_mqtt()
    connections.logger.debug(f"Temp data saved to mqtt (t={temp_data.temp_value}º, h={temp_data.humidity_value}%)")
    s.enter(20, 1, save_data_to_mqtt, (sc,))


s.enter(20, 1, save_data_to_mqtt, (s,))
s.run()
print("Hello world!")
