from dataclasses import dataclass, asdict
from json import dumps, loads
from typing import Optional


@dataclass
class Storage:
    lights_r: int = 0
    lights_g: int = 0
    lights_b: int = 0
    light_economic_mode: bool = True
    heater_threshold: int = 18
    cooler_threshold: int = 23
    alert_threshold: int = 70

    def save(self):
        json = dumps(asdict(self))
        with open("storage.json", "w+") as storage_file:
            storage_file.write(json)

    def save_cooler_threshold(self, value):
        self.cooler_threshold = value
        self.save()

    def save_heater_threshold(self, value):
        self.heater_threshold = value
        self.save()

    def save_alert_threshold(self, value):
        self.alert_threshold = value
        self.save()

    def load(self):
        try:
            with open("storage.json", "r+") as storage_file:
                data = storage_file.read()
                if data:
                    as_dict = loads(data)
                    print(as_dict)
                    for key, value in as_dict.items():
                        setattr(self, key, value)
        except FileNotFoundError:
            pass


global storage
storage = Storage()
