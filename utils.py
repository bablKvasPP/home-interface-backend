from settings import MQTT_ROOT_TOPIC


def generate_topic(topic_name: str):
    if topic_name.startswith("/"):
        return MQTT_ROOT_TOPIC + topic_name
    return f"{MQTT_ROOT_TOPIC}/{topic_name}"
