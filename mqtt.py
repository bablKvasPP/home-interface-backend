from hardware_components import hardware
from mqtt_routing import MqttRoute, find_route
from storage import storage
from utils import generate_topic

message_routes = [
    MqttRoute("lights/r", lambda x: hardware.rgb_led.set_rgb(r=int(x))),
    MqttRoute("lights/g", lambda x: hardware.rgb_led.set_rgb(g=int(x))),
    MqttRoute("lights/b", lambda x: hardware.rgb_led.set_rgb(b=int(x))),
    MqttRoute("heater/threshold/temperature", lambda x: storage.save_heater_threshold(int(x))),
    MqttRoute("fan/threshold/temperature", lambda x: storage.save_cooler_threshold(int(x))),
    MqttRoute("fan/alert", lambda x: storage.save_alert_threshold(int(x))),
]


def publish_message(topic, payload):
    from connections import connections
    connections.mqtt_client.publish(generate_topic(topic), payload=payload, retain=True)


def subscribe(topic_name):
    from connections import connections
    connections.logger.debug(f"Subscribed for {generate_topic(topic_name)} topic")
    connections.mqtt_client.subscribe(generate_topic(topic_name), 1)


def on_message(client, userdata, message):
    from connections import connections
    connections.logger.info("Received message '" + str(message.payload) + "' on topic '"
                            + message.topic + "' with QoS " + str(message.qos))
    route = find_route(message_routes, message.topic)
    if route:
        route.callback(message.payload.decode("utf-8"))
