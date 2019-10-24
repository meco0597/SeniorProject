// MotorController source
 
#include <Arduino.h>
#include "MotorController.h"

MotorController::MotorController(int _a1, int _a2, int _b1, int _b2){
  a1 = _a1;
  a2 = _a2;
  b1 = _b1;
  b2 = _b2;
  throttle = PWMRANGE;
  c1Voltage = 0;
  c2Voltage = 0;
  c1Goal = 0;
  c2Goal = 0;
  stopped = false;
}
 
void MotorController::setGoal(int g1, int g2) {
  c1Goal = max(min(g1, PWMRANGE), -PWMRANGE);
  c2Goal = max(min(g2, PWMRANGE), -PWMRANGE);
}

void MotorController::setMotors() {
  // Set all pins if stopped
  if (stopped) {
      analogWrite(a1, PWMRANGE);
      analogWrite(a2, PWMRANGE);
      analogWrite(b1, PWMRANGE);
      analogWrite(b2, PWMRANGE); 

     return;
  }

  // Checks for negative voltages and restricts it to motorThrottle
  analogWrite(a1, (c1Voltage < 0) ? min(abs(c1Voltage), throttle) : 0);
  analogWrite(a2, (c1Voltage < 0) ? 0 : min(abs(c1Voltage), throttle));
  analogWrite(b1, (c2Voltage < 0) ? min(abs(c2Voltage), throttle) : 0);
  analogWrite(b2, (c2Voltage < 0) ? 0 : min(abs(c2Voltage), throttle));  
}

// Immediately sets the pins without interpolation
void MotorController::updateVoltage() { 
  c1Voltage = c1Goal;
  c2Voltage = c2Goal;

  setMotors();
}

// Linerally interpolates the current and goal voltage with delta
void MotorController::updateVoltage(float delta) {
  int deltaV1 = (int)ceil(delta * (c1Goal - c1Voltage));
  int deltaV2 = (int)ceil(delta * (c2Goal - c2Voltage));
  c1Voltage = max(min(c1Voltage + deltaV1, PWMRANGE), -PWMRANGE);
  c2Voltage = max(min(c2Voltage + deltaV2, PWMRANGE), -PWMRANGE);
  
  setMotors();
}

void MotorController::setThrottle(int t) {
  throttle = min(abs(t), PWMRANGE);
}

void MotorController::toggleStop() {
  stopped = !stopped;
}
