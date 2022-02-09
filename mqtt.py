from utils import generate_topic


def publish_message(topic, payload):
    from connections import connections
    connections.mqtt_client.publish(generate_topic(topic), payload=payload, retain=True)


def subscribe(topic_name):
    from connections import connections
    connections.mqtt_client.subscribe(generate_topic(topic_name), 1)


def on_message(client, userdata, message):
    from connections import connections
    connections.logger.info("Received message '" + str(message.payload) + "' on topic '"
                            + message.topic + "' with QoS " + str(message.qos))
