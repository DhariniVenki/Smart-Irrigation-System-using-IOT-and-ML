
import paho.mqtt.client as mqtt
import pandas as pd
from joblib import load
import time

# Load the trained model
model = load('C:/Users/dhari/Desktop/IOT_Automatic_Irrigation/server/soil_moisture_model.pkl')# Adjust path as needed

# MQTT settings
MQTT_BROKER = "broker.hivemq.com"  # Example public broker
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"

# Define column names matching your model's expectations (excluding 'Status')
COLUMN_NAMES = ['Soil Moisture', 'Temperature', ' Soil Humidity', 'Air temperature', 'Wind speed', 'Air humidity', 'Wind gust ', 'Pressure ', 'pH', 'Rainfall', 'N', 'P', 'K']
# Callback when a message is received
def on_message(client, userdata, message):
    try:
        raw_data = message.payload.decode()
        print(f"Raw message payload: {raw_data}")

        # Parse the CSV string
        data_values = [float(value) for value in raw_data.split(',')]

        # Convert the data to a DataFrame
        df = pd.DataFrame([data_values], columns=COLUMN_NAMES)

        # Predict using the model
        prediction = model.predict(df)
        print(f"Received data: {data_values}")
        print(f"Prediction: {prediction}")
    except ValueError as e:
        print(f"Failed to parse data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Set up the MQTT client
client = mqtt.Client()

# Attach the on_message callback
client.on_message = on_message

# Attempt to connect to the broker
connected = False
tries = 0
while not connected and tries < 3:  # Try 3 times
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        connected = True
        print("Connected to MQTT broker.")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        tries += 1
        time.sleep(5)  # Wait for 5 seconds before retrying

if not connected:
    print("Unable to connect to MQTT broker after multiple attempts. Check network settings.")
    exit(1)

# Subscribe to the topic
client.subscribe(MQTT_TOPIC)

# Start the MQTT client loop
client.loop_forever()


