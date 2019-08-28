// Driver can be found here:
// https://www.sony.com/electronics/support/downloads/W0009576
// Not sure if it actually works

// Required settings to program:
// Board: Generic ESP8266 Module
// Crystal Frequency: 26 MHz
// Reset Method: nodemcu

// Idea: broadcast datagrams for all robots in a single packet 
// would reduce overhead massively


#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

/******************* Constants *******************/
const char* HUB_SSID = "";
const char* HUB_PASSWORD = "";
const IPAddress BROADCAST_ADDRESS(192, 168, 1, 255);
const unsigned int UDP_PORT = 5050; 
const unsigned int MAX_PACKET_SIZE  = 255;
/*************************************************/

/******************* Commands  *******************/
const byte ASSIGN = 1;
/*************************************************/

/******************** Globals ********************/
WiFiUDP UDP;
unsigned int robotID = 0;
 
/*************************************************/

void setup() {
  Serial.begin(115200);
  
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
  UDP.begin(UDP_PORT);
  Serial.println("Listening on port " + String(UDP_PORT));
  
  pinMode(0, OUTPUT); 
}

// Retrieves a command from a UDP packet
byte get_command() {
  char packet[MAX_PACKET_SIZE];
  int len = UDP.read(packet, MAX_PACKET_SIZE);

  // Unicast address is used for ID assignment
  if (UDP.destinationIP() != BROADCAST_ADDRESS && packet[0] == ASSIGN) {
      robotID = (int)packet[1];
      Serial.println("Assigned ID " + String(robotID));
  }
  
  // Process packet to determine command
  byte cmd = 0;
  for (int i = 0; i < len; i += 2) {
    if (packet[i] == robotID)
      cmd = packet[i + 1];  
  }
  
  return cmd;
}

// Sends information back to the hub 
void send_data(byte* data, int len) {
  UDP.beginPacket(UDP.remoteIP(), UDP.remotePort());
  UDP.write(data, len);
  UDP.endPacket();
}

void loop() {
  // Poll for commands from the hub
  byte cmd = 0;
  if (UDP.parsePacket())
    cmd = get_command();

  // The zero command does nothing
  if (cmd != 0) {
    Serial.println("Received command " + String((int)cmd));
  }
    
  digitalWrite(0, HIGH); // sets the digital pin 13 on
  delay(10);            // waits for a second
  digitalWrite(0, LOW);  // sets the digital pin 13 off
  delay(10);            // waits for a second
}
