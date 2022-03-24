from datetime import datetime
from typing import Callable

from RPi import GPIO


class DoorLock:
    def __init__(self, digital_tick_pin, success_led, failed_led, checking_led, tick_led, on_success: Callable,
                 etalon=None, threshold=0.35, timeout=7):
        self.etalon = [1, 1, 2] if etalon is None else etalon
        self.success_led = success_led
        self.checking_led = checking_led
        self.tick_led = tick_led
        self.failed_led = failed_led
        self.digital_tick_pin = digital_tick_pin
        GPIO.setup(digital_tick_pin, GPIO.IN)
        GPIO.add_event_detect(2, GPIO.RISING)
        GPIO.add_event_callback(2, self.get_tick_callback())
        self.combinations = []
        self.timeout = timeout
        self.threshold = threshold
        self.previous_measurement = datetime.now().timestamp()
        self.on_success = on_success
        self.is_success_callback_called = False

    def clear_old_combinations(self):
        from connections import connections
        self.combinations = list(
            filter(lambda x: datetime.now().timestamp() - x[0] < self.timeout, self.combinations))
        connections.logger.debug("Clearing old combinations")
        if self.combinations:
            self.failed_led.on()
            self.checking_led.off()

    def timings(self):
        timings_list = []
        for combination in self.combinations:
            current_timings = []
            if len(combination) >= 2:
                for i in range(0, len(combination) - 1):
                    current_timings.append(combination[i + 1] - combination[i])
            if current_timings:
                timings_list.append(current_timings)
        return timings_list

    def exists_correct_combinations(self):
        combination_timings = self.timings()
        for combination in combination_timings:
            is_correct = False
            if len(combination) == len(self.etalon):
                is_correct = True
                print(combination)
                for etalon_timing_index in range(len(self.etalon)):
                    if not ((1 + self.threshold) > (combination[etalon_timing_index]) / self.etalon[
                        etalon_timing_index] > (
                                    1 - self.threshold)):
                        is_correct = False
            if is_correct:
                return True
        return False

    def get_tick_callback(self):
        from connections import connections

        def tick_callback(_):
            if not self.is_success_callback_called:
                self.tick_led.on()
                if not self.combinations:
                    self.failed_led.off()
                    self.checking_led.on()
                if datetime.now().timestamp() - self.previous_measurement > 0.5:
                    now = round(datetime.now().timestamp(), 4)
                    for index in range(len(self.combinations)):
                        self.combinations[index].append(now)
                    self.combinations.append([now])
                    self.previous_measurement = now
                if self.exists_correct_combinations():
                    if not self.is_success_callback_called:
                        connections.logger.debug("Correct combination flag is setted true")
                        self.is_success_callback_called = True
                        connections.logger.info("Correct combinations found!")
                        self.combinations = []
                        self.checking_led.off()
                        self.success_led.on()
                        self.tick_led.off()
                        self.on_success()
                        self.success_led.off()
                        self.failed_led.on()
                        self.is_success_callback_called = False
                else:
                    self.tick_led.off()

        return tick_callback
