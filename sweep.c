#include <Servo.h>  // Include the Servo library

Servo myServo;  // Create Servo object to control servo motor
int servoPin = 9;  // Pin connected to the servo motor

void setup() {
  myServo.attach(servoPin);  // Attach the servo motor to pin 9
}

void loop() {
  // Sweep the servo motor from 0 to 180 degrees
  for (int pos = 0; pos <= 180; pos += 5) {
    myServo.write(pos);  // Move the servo to the 'pos' position
    delay(20);           // Wait for the servo to reach the position
  }

  // Sweep the servo motor from 180 back to 0 degrees
  for (int pos = 180; pos >= 0; pos -= 5) {
    myServo.write(pos);  // Move the servo to the 'pos' position
    delay(20);           // Wait for the servo to reach the position
  }
}