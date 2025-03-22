import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/temperature"

client = mqtt.Client()

client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    temperature = round(random.uniform(25.0, 35.0), 1)  # Sinh nhiệt độ ngẫu nhiên
    data = {
        "sensor_id": 1,
        "temperature": temperature,
        "timestamp": datetime.utcnow().isoformat()
    }
    json_data = json.dumps(data)
    
    print(f"Publishing: {json_data}")
    client.publish(MQTT_TOPIC, json_data)

    time.sleep(1)
