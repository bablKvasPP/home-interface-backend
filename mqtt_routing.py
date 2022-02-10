from typing import List

from utils import generate_topic


class MqttRoute:
    def __init__(self, topic, callback):
        self.topic = topic
        self.callback = callback


def find_route(routes: List[MqttRoute], topic):
    for route in routes:
        if generate_topic(route.topic) == topic:
            return route
