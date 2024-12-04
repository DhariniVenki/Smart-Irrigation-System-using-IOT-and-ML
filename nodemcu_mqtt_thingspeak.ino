#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "YourWiFiSSID";
const char* password = "YourWiFiPassword";
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* topic = "irrigation/sensors";
const char* motor_control_topic = "irrigation/motor";
const char* thingspeak_server = "api.thingspeak.com";
String api_key = "YOUR_THINGSPEAK_WRITE_API_KEY";

#define DHTPIN D1
#define SOIL_MOISTURE_PIN A0
#define PH_PIN A1
#define RAIN_PIN A2
#define NPK_PIN A3
#define RELAY_PIN D2

#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);
HTTPClient http;

float soilMoisture = 0;
float temperature = 0;
float humidity = 0;
float rain = 0;
float pH = 0;
float nitrogen = 0;
float phosphorus = 0;
float potassium = 0;

void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void connectMQTT() {
  while (!client.connected()) {
    client.connect("NodeMCUClient");
    if (client.connected()) client.subscribe(motor_control_topic);
    else delay(5000);
  }
}

void readSensors() {
  soilMoisture = analogRead(SOIL_MOISTURE_PIN) / 1023.0 * 100;
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();
  rain = analogRead(RAIN_PIN) / 1023.0 * 100;
  pH = analogRead(PH_PIN) / 1023.0 * 14;
  nitrogen = analogRead(NPK_PIN) / 1023.0 * 100;
  phosphorus = analogRead(NPK_PIN) / 1023.0 * 100;
  potassium = analogRead(NPK_PIN) / 1023.0 * 100;
}

void publishToMQTT() {
  char payload[512];
  sprintf(payload, "{\"SoilMoisture\": %.2f, \"Temperature\": %.2f, \"Humidity\": %.2f, \"Rainfall\": %.2f, \"pH\": %.2f, \"N\": %.2f, \"P\": %.2f, \"K\": %.2f}", 
          soilMoisture, temperature, humidity, rain, pH, nitrogen, phosphorus, potassium);
  client.publish(topic, payload);
}

void publishToThingSpeak() {
  String url = String("/update?api_key=") + api_key +
               "&field1=" + String(soilMoisture) +
               "&field2=" + String(temperature) +
               "&field3=" + String(humidity) +
               "&field4=" + String(rain) +
               "&field5=" + String(pH) +
               "&field6=" + String(nitrogen) +
               "&field7=" + String(phosphorus) +
               "&field8=" + String(potassium);
  http.begin("http://" + String(thingspeak_server) + url);
  http.GET();
  http.end();
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) message += (char)payload[i];
  if (message == "ON") digitalWrite(RELAY_PIN, LOW);
  else if (message == "OFF") digitalWrite(RELAY_PIN, HIGH);
}

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  dht.begin();
  connectWiFi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) connectMQTT();
  client.loop();
  readSensors();
  publishToMQTT();
  publishToThingSpeak();
  delay(15000);
}
