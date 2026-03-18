#include <ESP32Servo.h>

Servo myServo;
int servoPin = 18; // connected to D18

void setup() {
  Serial.begin(115200);
  myServo.attach(servoPin);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int angle = data.toInt();

    angle = constrain(angle, 0, 180);
    myServo.write(angle);
  }
}