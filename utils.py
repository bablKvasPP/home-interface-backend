from settings import MQTT_ROOT_TOPIC


def generate_topic(topic_name: str):
    return MQTT_ROOT_TOPIC + topic_name
