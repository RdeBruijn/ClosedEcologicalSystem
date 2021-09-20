#include <dht.h>
#include <BH1750.h>
#include <Wire.h>

dht DHT;
BH1750 lightMeter(0x23);

#define DHT11_PIN 7

void setup() {
  pinMode(A1, INPUT);
  Serial.begin(9600);
  Wire.begin();
  if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE_2)) {
    //Serial.println(F("BH1750 Advanced begin"));
  }
  else {
    //Serial.println(F("Error initialising BH1750"));
  }
}

void loop() {
  if (Serial.available()) {
    Serial.read();
    int chk = DHT.read11(DHT11_PIN);
    Serial.print("Arduino;");
    Serial.print("Arduino 1(inside of closed box);");
    Serial.print("Temperature;");
    Serial.print(DHT.temperature);
    Serial.print(";Humidity;");
    Serial.print(DHT.humidity);
    float lux = lightMeter.readLightLevel();
    Serial.print(";Light;");
    Serial.print(lux);
    int a = analogRead(A1);
    Serial.print(";Raw ground humidity;");
    Serial.print(a);
    a = map(a, 1023, 0, 0, 1023);
    a = map(a, 0, 485, 0, 100);
    a = min(100, a);
    a = max(0, a);
    Serial.print(";Ground humidity;");
    Serial.println(a);
  }

}
