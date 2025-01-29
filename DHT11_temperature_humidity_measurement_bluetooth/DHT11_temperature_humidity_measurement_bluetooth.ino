// Measure temp and humidity using a python script, transfer data using bluetooth

#include <BluetoothSerial.h>
#include <DHT.h>
#include <DHT_U.h>

BluetoothSerial SerialBT;

#define DHTPIN 17
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE); // constructor to declare sensor

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_DHT11"); // Bluetooth device name
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
    Serial.println("nan,nan");
    SerialBT.println("nan,nan");
    return;
  }

  // Print csv line: "humidity,temperature"
  Serial.print(h);
  Serial.print(",");
  Serial.println(t);

  SerialBT.print(h);
  SerialBT.print(",");
  SerialBT.println(t);

}
