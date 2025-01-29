// Measure temp and humidity using a python script

#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 17
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE); // constructor to declare sensor

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  // Delay 1000 milli seconds
  delay(1000);
  // Read humidity
  float h = dht.readHumidity();
  // Read temperature in Celsius
  float t = dht.readTemperature();

  // Returns an error if ESP32 does not receive measurement
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed reception");
    return;
  }

  // Print csv line: "humidity,temperature"
  Serial.print(h);
  Serial.print(",");
  Serial.println(t);

}
