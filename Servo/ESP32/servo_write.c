#include <ESP32Servo.h> // Include Servo library

Servo myServo;     // Create a Servo object
int servoPin = 18; // GPIO18 / D18

void setup() {
  myServo.attach(servoPin); // Attach servo to D18
}

void loop() {
  myServo.write(0);   // Move servo to 0 degrees
  delay(2000);        // Wait for 2 seconds
  myServo.write(180); // Move servo to 180 degrees
  delay(5000);        // Wait for 5 seconds
}
