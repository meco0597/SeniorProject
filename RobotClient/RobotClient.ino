// Required settings to program:
// Board: Generic ESP8266 Module
// Crystal Frequency: 26 MHz
// Reset Method: nodemcu

void setup() {
  // put your setup code here, to run once:
  pinMode(0, OUTPUT);    // sets the digital pin 13 as output
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(0, HIGH); // sets the digital pin 13 on
  delay(1000);            // waits for a second
  digitalWrite(0, LOW);  // sets the digital pin 13 off
  delay(1000);            // waits for a second
  Serial.println("X");
}
