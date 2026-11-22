#define BLYNK_TEMPLATE_ID "TMPL3yxfKbG6M"
#define BLYNK_TEMPLATE_NAME "PesticideSprinkle"
#define BLYNK_AUTH_TOKEN "YOUR_BLYNK_AUTH_TOKEN" // Set locally; don't commit real credentials

#define BLYNK_PRINT Serial
#include <WiFi.h>
#include <BlynkSimpleEsp32.h>

char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "YOUR_WIFI_SSID";     // Set locally; don't commit real credentials
char pass[] = "YOUR_WIFI_PASSWORD"; // Set locally; don't commit real credentials

int relayPin = 26;  // GPIO 26 connected to Relay

BLYNK_WRITE(V1) {
  int lockState = param.asInt();
  if (lockState == 1) {
    digitalWrite(relayPin, HIGH);
    Serial.println("Motor ON !");
  } else {
    digitalWrite(relayPin, LOW);
    Serial.println("Motor OFF !");
  }
}

void setup() {
  Serial.begin(115200);
  Blynk.begin(auth, ssid, pass);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);
}

void loop() {
  Blynk.run();
}
