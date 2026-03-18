#include <ESP32Servo.h> // Include Servo library

Servo myServo;    // Create Servo object
int servoPin = 18; // GPIO18 / D18

void setup() {
  myServo.attach(servoPin); // Attach servo to D18
}

void loop() {
  // Sweep servo from 0 to 180 degrees
  for (int pos = 0; pos <= 180; pos += 5) {
    myServo.write(pos); // Move servo to the 'pos' position
    delay(20);          // Wait for servo to reach position
  }
  // Sweep servo from 180 back to 0 degrees
  for (int pos = 180; pos >= 0; pos -= 5) {
    myServo.write(pos); // Move servo to the 'pos' position
    delay(20);          // Wait for servo to reach position
  }
}