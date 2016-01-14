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
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet,
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
		Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
		Serial.print("Contents:");
		Serial.println(packetBuffer);

		// send a reply, to the IP address and port that sent us the packet we just got
		Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
		Udp.write(replyBuffer);
		Udp.endPacket();
	}
	delay(10);
}
