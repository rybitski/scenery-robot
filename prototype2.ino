/*
This program is able to constantly read commands from an
xbox controller. It immediately turns the motors according
to those values. While it's turning, it's also recording the
encoder ticks generated by these turns.
*/

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
	Serial.println("Starting.");

	// put your setup code here, to run once:
	Serial.begin(9600);

	Serial.println("Continue.");

	// Set chip select high (inactive) for SD card.
	pinMode(SDCARD_CS_PIN, OUTPUT);
	digitalWrite(SDCARD_CS_PIN, HIGH);

	// if (Ethernet.begin(mac) == 0) {
	// 	Serial.println("Failed to configure Ethernet using DHCP.");
	// 	while (1);
	// }

	Ethernet.begin(mac, ip);

	// get and print our IP address
	Serial.println(Ethernet.localIP());

	Serial.println("Done with setup()!");
}

void loop() {
	// put your main code here, to run repeatedly:


}
