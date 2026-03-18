#include <Servo.h> // Include Servo library

Servo myServo;     // Create a Servo object
int servoPin = D2; // GPIO4

void setup() {
  myServo.attach(servoPin); // Attach servo to pin D2
}

void loop() {
  myServo.write(0);   // Move servo to 0 degrees
  delay(2000);        // Wait for 2 seconds
  myServo.write(180); // Move servo to 180 degrees
  delay(5000);        // Wait for 5 seconds
}
