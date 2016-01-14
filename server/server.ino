/*
This program runs a server on the main computer that controls
the robot(s). Eventually this code will be ported to Python
with a nice GUI.
*/

#include <Servo.h>
#include <SPI.h>
#include <EthernetV2_0.h>

const int SDCARD_CS_PIN = 4;
const int W5200_CS_PIN = 10;

// server stuff
byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0xD4, 0xE8 };
const int PORT = 29282;
IPAddress ip(192, 168, 1, 2);

// buffers for receiving and sending data
char packetBuffer[33]; //buffer to hold incoming packet,
char replyBuffer[] = "acknowledged";       // a string to send back

EthernetUDP Udp;

void setup() {
	Serial.begin(9600);

	Serial.println("Begin setup()");
	Serial.println("We are the server!");

	// Set chip select high (inactive) for SD card.
	pinMode(SDCARD_CS_PIN, OUTPUT);
	digitalWrite(SDCARD_CS_PIN, HIGH);

	// start the Ethernet connection:
	Serial.print("Configuring Ethernet client using static IP... ");
	Ethernet.begin(mac, ip);
	Serial.print("Success. ");

	delay(1000); // give the Ethernet sheild a second to initialize

	// get and print our IP address
	Serial.print("(Our IP: ");
	Serial.print(Ethernet.localIP());
	Serial.println(")");
	Serial.println();

	Udp.begin(PORT);
	
	Serial.println("Done with setup()");
}

void loop() {
	// if there's data available, read a packet
	int packetSize = Udp.parsePacket();
	if (packetSize) {
		// read the packet into the buffer
		Udp.read(packetBuffer, 12);
		// Serial.print("Our time: ");
		// Serial.print(millis());
		// Serial.print(" - Contents(");
		// Serial.print(packetSize);
		// Serial.print("):");
		unsigned long time = packetBuffer[0];
		signed long enc1 = packetBuffer[4];
		signed long enc2 = packetBuffer[8];
		Serial.print("Time=");
		Serial.print(time);
		Serial.print(" enc1=");
		Serial.print(enc1);
		Serial.print(" enc2=");
		Serial.println(enc2);


		// send a reply, to the IP address and port that sent us the packet we just got
		Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
		Udp.write(replyBuffer);
		Udp.endPacket();
	}
	delay(1);
}
