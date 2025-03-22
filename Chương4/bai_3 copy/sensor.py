import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/temperature"

sensor_id = random.randint(1, 100)  # Mỗi sensor có ID khác nhau
client = mqtt.Client()

client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    temperature = round(random.uniform(25.0, 35.0), 1)
    data = {
        "sensor_id": sensor_id,
        "temperature": temperature,
        "timestamp": datetime.utcnow().isoformat()
    }
    json_data = json.dumps(data)
    
    print(f"Sensor {sensor_id} publishing: {json_data}")
    client.publish(MQTT_TOPIC, json_data)

    time.sleep(1)
