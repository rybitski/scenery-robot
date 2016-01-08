#include <Servo.h>
#include <SPI.h>
#include <EthernetV2_0.h>

const int SDCARD_CS_PIN = 10;

Servo leftMotor;
Servo rightMotor;

// server stuff
boolean lastConnected = false;
String currentLine;
byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0xD4, 0xE7 };
IPAddress ip(192, 162, 1, 177);

EthernetClient client;

void setup() {
	// put your setup code here, to run once:
	Serial.begin(9600);

	// Set chip select high (inactive) for SD card.
	pinMode(SDCARD_CS_PIN, OUTPUT);
	digitalWrite(SDCARD_CS_PIN, HIGH);

	// get and print our IP address
	Serial.println(Ethernet.localIP());

	Serial.println("Done with setup()!");
}

void loop() {
	// put your main code here, to run repeatedly:


}
