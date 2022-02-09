from logging import getLogger, Logger

import coloredlogs
from paho.mqtt.client import Client

from settings import MQTT_PORT, MQTT_HOST, MQTT_USER, MQTT_PASSWORD


class Connections:
    mqtt_client: Client
    logger: Logger

    def initialize(self):
        self.logger = getLogger("hib")
        coloredlogs.install(level='DEBUG', logger=self.logger)
        self.logger.debug("Logger initialized")
        self.mqtt_client = Client()
        if MQTT_USER is not None and MQTT_PASSWORD is not None:
            self.mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        self.logger.debug(f"Connection to mqtt broker - {MQTT_HOST}:{MQTT_PORT}")
        self.mqtt_client.connect(MQTT_HOST, MQTT_PORT)
        self.logger.info("Connection to logger succeed")

    def setup_subscriptions(self):
        self.mqtt_client.subscribe()

global connections
connections = Connections()
