/*
This program runs a server on the main computer that controls
the robot(s). Eventually this code will be ported to Python
with a nice GUI.
*/

#include <Servo.h>
#include <SPI.h>
#include <EthernetV2_0.h>

const int SDCARD_CS_PIN = 4;

// server stuff
byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0xD4, 0xE8 };
const int PORT = 29281;
IPAddress ip(192, 168, 1, 2);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
EthernetServer server(PORT);
boolean gotAMessage = false; // whether or not you got a message from the client yet

typedef enum {receiveHeader, receiveLeft, receiveRight} ReceiveState;
ReceiveState receiveState;

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
	
	Serial.println("Done with setup()");
}

void loop() {
	// Gets a client that is connected to the server and has data
	// available for reading. The connection persists when the returned
	// client object goes out of scope; you can close it by calling 
	// client.stop().
	EthernetClient client = server.available();

	if (client) {
			client.write(0xA5);
			client.write(103);
			client.write(23);
		

	  	char thisChar = client.read();
	  	Serial.print(thisChar);
	}

	delay(200);
}
