import paho.mqtt.client as mqtt
import time
import random

# MQTT settings
broker = "broker.hivemq.com"
port = 1883
topic = "sensor/data"

client = mqtt.Client()
client.connect(broker, port, 60)

def simulate_data():
    while True:
        soilMoisture = random.uniform(0, 100)
        temperature = random.uniform(0, 50)
        soilHumidity = random.uniform(0, 70)
        airTemperature = random.uniform(0, 40)
        windSpeed = random.uniform(0, 20)
        airHumidity = random.uniform(20, 80)
        windGust = random.uniform(0, 30)
        pressure = random.uniform(90, 110)
        pH = random.uniform(0, 8)
        rainfall = random.uniform(0, 500)
        N = random.uniform(10, 100)
        P = random.uniform(5, 100)
        K = random.uniform(10, 100)

        payload = f"{soilMoisture},{temperature},{soilHumidity},{airTemperature},{windSpeed},{airHumidity},{windGust},{pressure},{pH},{rainfall},{N},{P},{K}"
        client.publish(topic, payload)
        print(f"Published: {payload}")
        time.sleep(5)

if __name__ == "__main__":
    simulate_data()
