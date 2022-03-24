import sched
import time

from connections import connections
from hardware_components import hardware
from light_sensor import THRESHOLD
from storage import storage
from temperature import get_temperature_data

connections.initialize()
hardware.initialize()
storage.load()
hardware.reinit()
s = sched.scheduler(time.time, time.sleep)


def save_temperature_to_mqtt(sc):
    temp_data = get_temperature_data()
    temp_data.save_to_mqtt()
    connections.logger.debug(f"Temp data saved to mqtt (t={temp_data.temp_value}º, h={temp_data.humidity_value}%)")
    hardware.reinit()
    s.enter(5, 1, save_temperature_to_mqtt, (sc,))


def alert_on_high(sc):
    temp_data = get_temperature_data()
    if temp_data.temp_value > storage.alert_threshold:
        hardware.buzzer.alert()
    else:
        hardware.buzzer.silence()
    s.enter(5, 1, alert_on_high, (sc,))

def cool_on_high_heat_on_cold(sc):
    temp_data = get_temperature_data()
    if temp_data.temp_value > storage.cooler_threshold:
        hardware.cooler.on()
    else:
        hardware.cooler.off()
    if temp_data.temp_value < storage.heater_threshold:
        hardware.heater.on()
    else:
        hardware.heater.off()
    s.enter(5, 1, cool_on_high_heat_on_cold, (sc,))


def save_illumination_to_mqtt(sc):
    illumination = hardware.light_sensor.read_data()
    illumination.save()
    connections.logger.debug(f"Lights saved to mqtt ({illumination.percents}%)")
    hardware.reinit()
    s.enter(5, 1, save_illumination_to_mqtt, (sc,))


def clear_old_combinations(sc):
    hardware.door_lock.clear_old_combinations()
    s.enter(5, 1, clear_old_combinations, (sc,))


def turn_lights_off_in_economic_mode(sc):
    illumination = hardware.light_sensor.read_data()
    if illumination.percents > THRESHOLD:
        hardware.rgb_led.turn_off()
        connections.logger.info("Turning led off")
    else:
        hardware.rgb_led.turn_on()
        connections.logger.info("Turning led on")
    s.enter(5, 1, turn_lights_off_in_economic_mode, (sc,))


s.enter(5, 1, save_temperature_to_mqtt, (s,))
s.enter(5, 1, alert_on_high, (s,))
s.enter(5, 1, save_illumination_to_mqtt, (s,))
s.enter(2, 1, cool_on_high_heat_on_cold, (s,))
s.enter(5, 1, clear_old_combinations, (s,))
s.enter(5, 1, turn_lights_off_in_economic_mode, (s,))
try:
    s.run()
except KeyboardInterrupt:
    connections.logger.error("Bye-Bye")
    connections.mqtt_client.loop_stop()
    hardware.stop()
    exit()
