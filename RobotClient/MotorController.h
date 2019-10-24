// MotorController header
// Used to control the DRV8835 with lots of helpful stuff

#ifndef MotorController_h
#define MotorController_h
 
#include <Arduino.h>
 
class MotorController {
public:
 MotorController(int _a1, int _a2, int _b1, int _b2);  // Channel pins
 void setGoal(int g1, int g2);
 void updateVoltage();
 void updateVoltage(float delta); // Interpolation function (linear)
 void setThrottle(int t);
 void toggleStop();
private:
 int a1, a2, b1, b2;
 int throttle;
 int c1Voltage, c2Voltage;
 int c1Goal, c2Goal; // Used for interpolation
 bool stopped;
 void setMotors();
};
 
#endif
