/*
This program runs a server on the main computer that controls
the robot(s). Eventually this code will be ported to Python
with a nice GUI.
*/

#include <Servo.h>
#include <SPI.h>
#include <EthernetV2_0.h>
#include <stdint.h>

const int SDCARD_CS_PIN = 4;
const int W5200_CS_PIN = 10;

// server stuff
byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0xD4, 0xE8 };
const int TCP_PORT = 29281;
const int UDP_PORT = 29282;
IPAddress ip(192, 168, 1, 2);
EthernetServer server(TCP_PORT);

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

	// start listening for clients
	server.begin();

	Udp.begin(UDP_PORT);
	
	Serial.println("Done with setup()");
}

void loop() {
	// if override button enabled
		// send UDP command for joysticks
	// if record button toggled
		// send UDP toggle record command
	// if button pressed to send path, send UDP path send command
		// then send TCP packet(s) with path
		// robot replays it
	// if button pressed to receive path, send UDP path return command
		// then receive TCP packet(s) with path

	// Gets a client that is connected to the server and has data
	// available for reading. The connection persists when the returned
	// client object goes out of scope; you can close it by calling 
	// client.stop().
	// EthernetClient client = server.available();

	// if (client) {
	//   	while(client.read());
	// }

	IPAddress destination(192, 168, 1, 3);
	Udp.beginPacket(destination, UDP_PORT);
	byte data[16];
	unsigned long now = millis();
	uint8_t data1 = 0x55;
	uint8_t data2 = 0x32;
	memcpy(data, &now, 4);
	memcpy(data + 4, &data1, 1);
	memcpy(data + 5, &data2, 1);
	Udp.write(data, 12);
	Udp.endPacket();

	Serial.print("Sent.");
}
