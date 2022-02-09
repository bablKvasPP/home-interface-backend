from dataclasses import dataclass, asdict
from json import dumps, loads
from typing import Optional


@dataclass
class Storage:
    lights_r: int = 0
    lights_g: int = 0
    lights_b: int = 0
    heater_threshold: int = 18
    cooler_threshold: int = 23

    def save(self):
        json = dumps(asdict(self))
        with open("storage.json", "w+") as storage_file:
            storage_file.write(json)

    def load(self):
        try:
            with open("storage.json", "r+") as storage_file:
                data = storage_file.read()
                if data:
                    as_dict = loads(data)
                    for key, value in as_dict.values():
                        setattr(self, key, value)
        except FileNotFoundError:
            pass


global storage
storage = Storage()
