import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/temperature"

TEMPERATURE_THRESHOLD = 30.0  # Ngưỡng cảnh báo

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    temperature = data["temperature"]

    print(f"Received data: Sensor {data['sensor_id']} - Temp: {temperature}°C - Time: {data['timestamp']}")

    if temperature > TEMPERATURE_THRESHOLD:
        print("⚠️ CẢNH BÁO: Nhiệt độ vượt ngưỡng!")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
