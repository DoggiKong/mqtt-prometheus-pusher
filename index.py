import os
import paho.mqtt.client as mqtt
import yaml
from dotenv import load_dotenv
from prometheus_client import CollectorRegistry, push_to_gateway, Gauge

# MQTT callback function
def on_message(client, userdata, msg):
    # Extract relevant data from the MQTT message
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    print(payload)
    # Transform MQTT data into Prometheus metrics
    # Here, we create a gauge metric and set its value

    # Set up Prometheus registry
    registry = CollectorRegistry()

    baseName = "mqtt:"

    gauge_metric = Gauge(baseName + topic, 'MQTT Data', ['topic'], registry=registry)
    gauge_metric.labels(topic=topic).set(float(payload))

    # Push metrics to Pushgateway
    push_to_gateway(os.environ.get('PUSHGATEWAY_ADDRESS'), job='pushgateway', registry=registry)

# load .env files
load_dotenv()

# Set up MQTT client
print("Connecting to MQTT client...")
client = mqtt.Client()
client.on_message = on_message
client.connect(os.environ.get('MQTT_ADDRESS'), int(os.environ.get('MQTT_PORT')), 60)

# Read the YAML file
with open('topics.yml', 'r') as file:
    yaml_data = yaml.safe_load(file)
    topics = yaml_data["topics"]

for topic in topics:
    topicName = topic["name"]
    topicTopic = topic["topic"]
    print(f"Subscribing to topic name: { topicName }, topic: { topicTopic }")
    client.subscribe(topicTopic)

# Start MQTT client loop
client.loop_start()
print("Connected to MQTT client")

# Wait for MQTT messages and push metrics to Pushgateway
try:
    while True:
        # Continue other operations if needed
        pass
finally:
    # Stop MQTT client loop
    client.loop_stop()
