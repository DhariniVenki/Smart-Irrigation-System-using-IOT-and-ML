import paho.mqtt.client as mqtt
import pandas as pd
import pickle
import json
import numpy as np

# MQTT configurations
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_SENSOR_TOPIC = "smart_irrigation/sensor_data"
MQTT_MOTOR_TOPIC = "smart_irrigation/motor_status"

# Load the trained model and scaler
with open("random_forest_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Function to preprocess data and make predictions
def predict_motor_status(sensor_data):
    # Extract features
    features = [
        sensor_data.get("SoilMoisture", 0),
        sensor_data.get("Temperature", 0),
        sensor_data.get("Humidity", 0),
        sensor_data.get("Rainfall", 0),
        sensor_data.get("pH", 0),
        sensor_data.get("N", 0),
        sensor_data.get("P", 0),
        sensor_data.get("K", 0),
    ]
    # Preprocess the features
    features_scaled = scaler.transform([features])
    # Predict using the model
    prediction = model.predict(features_scaled)
    return "ON" if prediction[0] == 1 else "OFF"

# Callback for when a message is received
def on_message(client, userdata, msg):
    try:
        # Decode the sensor data
        sensor_data = json.loads(msg.payload.decode())
        print(f"Received sensor data: {sensor_data}")
        
        # Predict motor status
        motor_status = predict_motor_status(sensor_data)
        print(f"Predicted Motor Status: {motor_status}")
        
        # Publish the motor status
        client.publish(MQTT_MOTOR_TOPIC, motor_status)
        print(f"Published Motor Status: {motor_status}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Initialize MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to the sensor data topic
client.subscribe(MQTT_SENSOR_TOPIC)

# Start the MQTT loop
print("MQTT Subscriber is running and waiting for sensor data...")
client.loop_forever()
