#include <Servo.h>
#include <SPI.h>
#include <EthernetV2_0.h>

const int SDCARD_CS_PIN = 4;

// server stuff
byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0xD4, 0xE8 };
const int PORT = 29281;
IPAddress ip(192, 168, 1, 3);
IPAddress gateway(192,168,1, 1);
IPAddress subnet(255, 255, 0, 0);
EthernetServer server(PORT);
boolean gotAMessage = false; // whether or not you got a message from the client yet

void setup() {
	Serial.begin(9600);

	Serial.println("Begin setup()");
	Serial.println("We are the server!");


	// Set chip select high (inactive) for SD card.
	pinMode(SDCARD_CS_PIN, OUTPUT);
	digitalWrite(SDCARD_CS_PIN, HIGH);

	// start the Ethernet connection:
	Serial.println("Trying to get an IP address using DHCP");
	if (Ethernet.begin(mac) == 0) {
	  Serial.println("Failed to configure Ethernet using DHCP");
	  // initialize the ethernet device not using DHCP:
	  Ethernet.begin(mac, ip, gateway, subnet);
	}
	// print your local IP address:
	Serial.print("My IP address: ");
	ip = Ethernet.localIP();
	for (byte thisByte = 0; thisByte < 4; thisByte++) {
	  // print the value of each byte of the IP address:
	  Serial.print(ip[thisByte], DEC);
	  Serial.print("."); 
	}
	Serial.println();
	// start listening for clients
	server.begin();
	
	Serial.println("Done with setup()");
}

void loop() {
  EthernetClient client = server.available();

  // when the client sends the first byte, say hello:
  if (client) {
    if (!gotAMessage) {
      Serial.println("We have a new client");
      client.println("Hello, client!"); 
      gotAMessage = true;
    }

    // read the bytes incoming from the client:
    char thisChar = client.read();
    // echo the bytes back to the client:
    server.write(thisChar);
    // echo the bytes to the server as well:
    Serial.print(thisChar);
  }
}
