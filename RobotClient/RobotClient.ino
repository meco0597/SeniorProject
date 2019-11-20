// Required settings to program:
// Board: Generic ESP8266 Module
// Crystal Frequency: 26 MHz
// CPU Frequency: 160 MHz
// Reset Method: nodemcu
// Flash Size: 4M (1M SPIFFS)

// Move command: 000011xx
// Parameter1 and parameter2 are for left and right motor speed respectively
// Note that the LSB of the command determines the direction of the right motor
// and the next bit determines the direction of the left motor (1 is forward)
// e.x. 00001110 is forward for the left motor and backwards for the right

// Read battery level: 0F 03 E8 00
// Set both motors to 500/1023 * vBat: 00 47 C1 F4

// Robot communication protocol:
// [ID] [COMMAND] [PARAMETER1] [PARAMETER2]
// [4 bits] [8 bits] [10 bits] [10 bits]
// 4 bytes total

// TODO: MPU library + integration
// TODO: Motor stall detection
// TODO: Read/Write operations
// TODO: Documentation :)

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ESP8266mDNS.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266httpUpdate.h>
#include <ArduinoOTA.h>
#include "MotorController.h"

/******************* Constants *******************/
const int FW_VERSION = 2;
const char* FW_URL = "http://192.168.1.66:8080/fota/";
const char* HUB_SSID = "HUBNETWORK";
const char* HUB_PASSWORD = "AlwaysAtFun";
const IPAddress BROADCAST_ADDRESS(192, 168, 1, 255);
const IPAddress MULTICAST_ADDRESS(224, 0, 0, 0);
#define UDP_PORT 5050
#define MAX_PACKET_SIZE  1023
#define AIN1_PIN 4
#define AIN2_PIN 5
#define BIN1_PIN 14
#define BIN2_PIN 16
#define I2C_SCL 12
#define I2C_SDA 13
#define PWM_MAX 1023 
#define MPU_INTERRUPT_PIN 2 
#define ID_SIZE 4
#define OP_SIZE 8
#define PARAM_SIZE 10
#define CMD_SIZE 32
#define BAT_ALPHA 0.95
#define MAX_BAT 4.3
/*************************************************/

/******************** Macros  ********************/
#define ID_POS (CMD_SIZE - ID_SIZE)
#define ID_MASK ((1 << ID_SIZE) - 1)
#define OP_POS (CMD_SIZE - (ID_SIZE + OP_SIZE))
#define OP_MASK ((1 << OP_SIZE) - 1)
#define PARAM1_POS (CMD_SIZE - (ID_SIZE + OP_SIZE + PARAM_SIZE))
#define PARAM_MASK ((1 << PARAM_SIZE) - 1)
/*************************************************/

/******************* Commands  *******************/
#define ASSIGN 0x01
#define UPDATE 0x02
#define MOVE 0x04
#define STOP 0x08
#define WRITE 0xE0
#define READ 0xF0
#define ACCEL_X 0xF1
#define ACCEL_Y 0xF2
#define ACCEL_Z 0xF3
#define ROT_X 0xF4
#define ROT_Y 0xF5
#define ROT_Z 0xF6
#define POS_X 0xF7
#define POS_Y 0xF8
#define POS_Z 0xF9
#define BAT_CHARGE 0xFA
#define TEMP 0xFB
#define THROTTLE 0xFC
#define LIGHT 0xFF
/*************************************************/

/******************** Globals ********************/
WiFiUDP UDP;
MotorController motorController(AIN1_PIN, AIN2_PIN, BIN1_PIN, BIN2_PIN);
unsigned int robotID = 0;
float batVoltage = 0;
/*************************************************/

struct RobotCommand {
  byte id;
  byte opCode;
  int16_t param1;
  int16_t param2;
};

void setup() {
  Serial.begin(115200);
  Serial.println("Current version: " + (String)FW_VERSION);
  
  // Connect to the hub
  WiFi.begin(HUB_SSID, HUB_PASSWORD);
  Serial.print("Connecting.");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("IP Address:\t");
  Serial.println(WiFi.localIP());

  // Start listening for UDP packets
  UDP.beginMulticast(WiFi.localIP(), MULTICAST_ADDRESS, UDP_PORT);
  Serial.println("Listening on port " + String(UDP_PORT));
  Serial.print("Subscribed to multicast address ");
  Serial.println(MULTICAST_ADDRESS);
  
  pinMode(0, OUTPUT);
  pinMode(2, OUTPUT); 
  digitalWrite(2, HIGH);
  
  // OTA updating stuff
  //ArduinoOTA.setPort(5051);
  //ArduinoOTA.begin();
}

void checkForUpdates() {
  Serial.println("Checking for firmware updates..." );

  HTTPClient httpClient;
  httpClient.begin((String)FW_URL + "robotclient.version");
  int httpCode = httpClient.GET();
  if( httpCode == 200 ) {
    String newFWVersion = httpClient.getString();
  
    if (newFWVersion.toInt() > FW_VERSION) {
      Serial.println("Updating to version " + newFWVersion);
      ESPhttpUpdate.update((String)FW_URL + "robotclient.bin");
    }
  }
  httpClient.end();
}

// Retrieves a command from a UDP packet
// Returns true if a command matches this robot's ID
bool getCommand(RobotCommand *cmd) {
  char packet[MAX_PACKET_SIZE];
  int len = UDP.read(packet, MAX_PACKET_SIZE);

  // Process packet to determine command
  for (int i = 0; i < len; i += 4) {
    if ((packet[i] >> (8 - ID_SIZE)) == robotID || UDP.destinationIP() != MULTICAST_ADDRESS) {
        // Put the packet into a 32-bit variable
        int32_t data = ((int32_t)packet[i] << 24) | ((int32_t)packet[i+1] << 16) | ((int32_t)packet[i+2] << 8) | (int32_t)packet[i+3];     

        // Retrive the parts through bitshifts and masks
        cmd->id = (data >> ID_POS) & ID_MASK;
        cmd->opCode = (data >> OP_POS) & OP_MASK;
        cmd->param1 = (data >> PARAM1_POS) & PARAM_MASK;
        cmd->param2 = data & PARAM_MASK;

        return true;
    }
  }

  return false;
}

// Sends information back to the hub 
void sendUDP(byte* data, int len) {
  UDP.beginPacket(UDP.remoteIP(), 5051);
  UDP.write(data, len);
  UDP.endPacket();
}

// Sends the requested information back to the hub
void sendInformation(RobotCommand *cmd) {
  // param1 determines what to send
  switch (cmd->param1) {
    case BAT_CHARGE:
      char data[4];
      dtostrf(batVoltage, 4, 2, data);
      sendUDP((byte*)data, 4);
      break;
  }
}

// Needs to be configured for different resistor values
float getBatVoltage() {
  return (analogRead(A0) / 1023.0) * 4.3;
}

void processRobotCommand() {
  RobotCommand cmd;
  
  if (getCommand(&cmd)) {
      Serial.println("Received command: ");
      Serial.println("ID: " + String((int)cmd.id));
      Serial.println("OpCode: " + String((int)cmd.opCode));
      Serial.println("Param1: " + String(cmd.param1));
      Serial.println("Param2: " + String(cmd.param2));

      // Check for normal operations
      switch (cmd.opCode) {
        case ASSIGN: 
          robotID = cmd.id;
          break;
        case UPDATE:
          checkForUpdates();
          break;
        case READ: 
          sendInformation(&cmd);
          break;
        case WRITE:
          switch (cmd.param1) {
            case THROTTLE:
              motorController.setThrottle(cmd.param2);
              break;
          }
        case LIGHT:
          analogWrite(2, PWMRANGE - cmd.param1);
          break;
        default:
          break;
      }

      // Check for motor operations
      switch (cmd.opCode & 0xFC) {
        case MOVE: {
          // Set and invert PWM goals based on direction
          int rightGoal = (cmd.opCode & 0x01) ? -(int)cmd.param2 : (int)cmd.param2;
          int leftGoal = (cmd.opCode & 0x02) ? -(int)cmd.param1 : (int)cmd.param1;

          // Scale goals based on current battery voltage
          // This allows the goal voltage to scale along with the battery voltage, so an almost dead robot won't be as slow as a fresh one
          rightGoal = rightGoal * (MAX_BAT / batVoltage);
          leftGoal = leftGoal * (MAX_BAT / batVoltage);
          
          motorController.setGoal(rightGoal, leftGoal);
          break;
        }
        case STOP:
          motorController.toggleStop();
          break;
        default:
          break;
      }
   }
}

void loop() {
  
  // Poll for commands from the hub
  if (UDP.parsePacket()) {
    processRobotCommand();
  }
  
  motorController.updateVoltage(0.25);
  batVoltage = (batVoltage * BAT_ALPHA) + (getBatVoltage() * (1 - BAT_ALPHA));

  digitalWrite(0, HIGH);

  delay(10); // Allows wifi code to run!

  digitalWrite(0, LOW);
}
