from connections import connections
from utils import generate_topic


def publish_message(topic, payload):
    connections.mqtt_client.publish(generate_topic(topic), payload=payload, retain=True)
