#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Wi-Fi credentials
const char* ssid = ""; // the one we will use make sure for wifi we have 2.4GHZ
const char* password = "pwd";

// MQTT broker
const char* mqtt_server = ""; // depends on the broker we use: do hostname -I in wsl
const char* topic = "ESIOT";

// LED pins
const int ledPins[] = {D0, D1, D2, D3, D4};
const int numLeds = sizeof(ledPins) / sizeof(ledPins[0]);

WiFiClient espClient;
PubSubClient client(espClient);

int lastCount = 0;
int imageCounter = 0;

void setup_wifi() {
  delay(10);
  Serial.begin(115200);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  int car_count = atoi((char*)payload);
  Serial.print("Received car count: ");
  Serial.println(car_count);
  
  // Check if a car/object is detected
  if (car_count > lastCount) {
    imageCounter++;
    if (imageCounter == 5) {
      // Decrease one LED if a car/object is detected after every 5 images
      for (int i = 0; i < numLeds; i++) {
        digitalWrite(ledPins[i], LOW);
        delay(100);  // Delay for stability
      }
      // Reset the image counter
      imageCounter = 0;
    }
  }
  // Update lastCount
  lastCount = car_count;
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      client.subscribe(topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  setup_wifi();
  
  // Initialize MQTT client
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
  // Initialize LED pins
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], HIGH); // Turn on all LEDs initially
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
