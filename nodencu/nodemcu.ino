#include <FirebaseESP8266.h>  // Include Firebase library
#include <ESP8266WiFi.h>
#include <DHT.h>


#define DHT_SENSOR_PIN  D7 // The ESP8266 pin D7 connected to DHT11 sensor
#define DHT_SENSOR_TYPE DHT11
#define BUZER D6

DHT dht_sensor(DHT_SENSOR_PIN, DHT_SENSOR_TYPE);

// Wi-Fi credentials
#define WIFI_SSID "your wifi"
#define WIFI_PASSWORD "your password

// Firebase configuration
#define FIREBASE_HOST "https://your database url.firebaseio.com/"
#define FIREBASE_AUTH "your api"

// Define Firebase data object
FirebaseData firebaseData;
FirebaseJson json;

// Define Firebase Config and Auth objects
FirebaseConfig config;
FirebaseAuth auth;

void setup() {
  Serial.begin(115200);  // Initialize serial monitor

  wifiConnect();

  // Assign Firebase host and auth details to the config object
  config.host = FIREBASE_HOST;
  config.signer.tokens.legacy_token = FIREBASE_AUTH;

  // Initialize Firebase
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  pinMode(BUZER, OUTPUT); // Initialize BUZER pin as OUTPUT

  dht_sensor.begin(); // Initialize the DHT sensor

  Serial.println("Firebase connected.");
}

void loop() {
  // Read humidity and temperature
  float humi = dht_sensor.readHumidity();
  float temperature_C = dht_sensor.readTemperature();
  float temperature_F = dht_sensor.readTemperature(true);

  // Check for notification
  

  // Check if sensor readings are valid
  if (isnan(temperature_C) || isnan(temperature_F) || isnan(humi)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    // Print sensor readings to Serial Monitor
    Serial.print("Humidity: ");
    Serial.print(humi);
    Serial.print("%  |  Temperature: ");
    Serial.print(temperature_C);
    Serial.print("°C  ~  ");
    Serial.print(temperature_F);
    Serial.println("°F");

    if (Firebase.getBool(firebaseData, "/notify")) {
    if (firebaseData.boolData() == true) { // Only execute if true
      // Set the pin high
      notify();
      }
  }

    // Send data to Firebase
    if (Firebase.setFloat(firebaseData, "/sensor/temperature_C", temperature_C)) {
      print_ok();
    } else {
      print_fail();
    }
    if (Firebase.setFloat(firebaseData, "/sensor/temperature_F", temperature_F)) {
      print_ok();
    } else {
      print_fail();
    }
    if (Firebase.setFloat(firebaseData, "/sensor/humi", humi)) {
      print_ok();
    } else {
      print_fail();
    }
  }

  // Wait 5 seconds before the next loop
  delay(5000);
}


void wifiConnect() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
}

void print_ok() {
  Serial.println("------------------------------------");
  Serial.println("OK");
  Serial.println("PATH: " + firebaseData.dataPath());
  Serial.println("TYPE: " + firebaseData.dataType());
  Serial.println("ETag: " + firebaseData.ETag());
  Serial.println("------------------------------------");
  Serial.println();
}

void print_fail() {
  Serial.println("------------------------------------");
  Serial.println("FAILED");
  Serial.println("REASON: " + firebaseData.errorReason());
  Serial.println("------------------------------------");
  Serial.println();
}

void notify() {
  // Activate the buzzer or LED
  digitalWrite(BUZER, HIGH);

  // Wait for 3 seconds
  delay(3000);

  // Deactivate the buzzer or LED
  digitalWrite(BUZER, LOW);

  // Update the notification status in Firebase
  if (!Firebase.setBool(firebaseData, "/notify", false)) {
    Serial.println("Failed to update notify status");
  }
}

