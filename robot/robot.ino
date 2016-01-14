/*
This program is able to constantly read commands from an
xbox controller. It immediately turns the motors according
to those values. While it's turning, it's also recording the
encoder ticks generated by these turns.
*/

#include <SPI.h>
#include <EthernetV2_0.h>
#include <EthernetUdpV2_0.h>
#include <Sabertooth.h>
#include <stdint.h>

const int SDCARD_CS_PIN = 4; // SD card chip select
const int W5200_CS_PIN = 10; // ethernet card chip select

// Slave Select pins for encoders 1 and 2
// Feel free to reallocate these pins to best suit your circuit
const int ENCODER_1_SS_PIN = 7;
const int ENCODER_2_SS_PIN = 8;

// These hold the current encoder count.
signed long encoder1Count = 0;
signed long encoder2Count = 0;

// server stuff
byte mac[] = {0x62, 0x02, 0x69, 0x9E, 0xC4, 0xFF};
const int PORT = 29282;
IPAddress ip(192, 168, 1, 3);
EthernetClient client;
EthernetUDP Udp;

const byte HEADER_BYTE = 0xA5;

// datastructure to hold the controls from the server
typedef struct {
	int8_t leftMotorPower; // between -127 and 127, to match Sabertooth controller
	int8_t rightMotorPower; // between -127 and 127, to match Sabertooth controller
	// byte deadManSwitch; // code to enable motors
} Controls;
Controls controls; // specific instance of struct

Sabertooth ST(128);

void initEncoders(void) {
	// Set slave selects as outputs
	pinMode(ENCODER_1_SS_PIN, OUTPUT);
	pinMode(ENCODER_2_SS_PIN, OUTPUT);

	// Raise select pins
	// Communication begins when you drop the individual select signsl
	digitalWrite(ENCODER_1_SS_PIN, HIGH);
	digitalWrite(ENCODER_2_SS_PIN, HIGH);

	SPI.begin();

	// Initialize encoder 1
	//    Clock division factor: 0
	//    Negative index input
	//    free-running count mode
	//    x4 quatrature count mode (four counts per quadrature cycle)
	// NOTE: For more information on commands, see datasheet
	digitalWrite(ENCODER_1_SS_PIN, LOW);        // Begin SPI conversation
	SPI.transfer(0x88);                       // Write to MDR0
	SPI.transfer(0x03);                       // Configure to 4 byte mode
	digitalWrite(ENCODER_1_SS_PIN, HIGH);       // Terminate SPI conversation

	// Initialize encoder 2
	//    Clock division factor: 0
	//    Negative index input
	//    free-running count mode
	//    x4 quatrature count mode (four counts per quadrature cycle)
	// NOTE: For more information on commands, see datasheet
	digitalWrite(ENCODER_2_SS_PIN, LOW);        // Begin SPI conversation
	SPI.transfer(0x88);                       // Write to MDR0
	SPI.transfer(0x03);                       // Configure to 4 byte mode
	digitalWrite(ENCODER_2_SS_PIN, HIGH);       // Terminate SPI conversation
}

long readEncoder(int encoder) {
	// Initialize temporary variables for SPI read
	unsigned int count1, count2, count3, count4;
	long countValue;

	// Read encoder 1
	if (encoder == 1) {
		digitalWrite(ENCODER_1_SS_PIN, LOW);      // Begin SPI conversation
		SPI.transfer(0x60);                     // Request count
		count1 = SPI.transfer(0x00);           // Read highest order byte
		count2 = SPI.transfer(0x00);
		count3 = SPI.transfer(0x00);
		count4 = SPI.transfer(0x00);           // Read lowest order byte
		digitalWrite(ENCODER_1_SS_PIN, HIGH);     // Terminate SPI conversation
	}

	// Read encoder 2
	else if (encoder == 2) {
		digitalWrite(ENCODER_2_SS_PIN, LOW);      // Begin SPI conversation
		SPI.transfer(0x60);                      // Request count
		count1 = SPI.transfer(0x00);           // Read highest order byte
		count2 = SPI.transfer(0x00);
		count3 = SPI.transfer(0x00);
		count4 = SPI.transfer(0x00);           // Read lowest order byte
		digitalWrite(ENCODER_2_SS_PIN, HIGH);     // Terminate SPI conversation
	}

	// Calculate encoder count
	countValue = (count1 << 8) + count2;
	countValue = (countValue << 8) + count3;
	countValue = (countValue << 8) + count4;

	return countValue;
}

void clearEncoderCount(void) {
	// Set encoder1's data register to 0
	digitalWrite(ENCODER_1_SS_PIN, LOW);      // Begin SPI conversation
	// Write to DTR
	SPI.transfer(0x98);
	// Load data
	SPI.transfer(0x00);  // Highest order byte
	SPI.transfer(0x00);
	SPI.transfer(0x00);
	SPI.transfer(0x00);  // lowest order byte
	digitalWrite(ENCODER_1_SS_PIN, HIGH);     // Terminate SPI conversation

	delayMicroseconds(100);  // provides some breathing room between SPI conversations

	// Set encoder1's current data register to center
	digitalWrite(ENCODER_1_SS_PIN, LOW);      // Begin SPI conversation
	SPI.transfer(0xE0);
	digitalWrite(ENCODER_1_SS_PIN, HIGH);     // Terminate SPI conversation

	// Set encoder2's data register to 0
	digitalWrite(ENCODER_2_SS_PIN, LOW);      // Begin SPI conversation
	// Write to DTR
	SPI.transfer(0x98);
	// Load data
	SPI.transfer(0x00);  // Highest order byte
	SPI.transfer(0x00);
	SPI.transfer(0x00);
	SPI.transfer(0x00);  // lowest order byte
	digitalWrite(ENCODER_2_SS_PIN, HIGH);     // Terminate SPI conversation

	delayMicroseconds(100);  // provides some breathing room between SPI conversations

	// Set encoder2's current data register to center
	digitalWrite(ENCODER_2_SS_PIN, LOW);      // Begin SPI conversation
	SPI.transfer(0xE0);
	digitalWrite(ENCODER_2_SS_PIN, HIGH);     // Terminate SPI conversation
}

void setup(void) {
	Serial.begin(9600);

	Serial.println("Begin setup()");
	Serial.println("We are the server!");

	initEncoders();       Serial.println("Encoders initialized.");
	clearEncoderCount();  Serial.println("Encoders cleared.");

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

void loop(void) {
	// Retrieve current encoder counters
	encoder1Count = readEncoder(1);
	encoder2Count = readEncoder(2);

	// Output state to serial monitor
	Serial.print("Enc1: ");
	Serial.print(encoder1Count);
	Serial.print(" Enc2: ");
	Serial.print(encoder2Count);

	Serial.print(" leftMotorPower: ");
	Serial.print(controls.leftMotorPower);
	Serial.print(" rightMotorPower: ");
	Serial.println(controls.rightMotorPower);

	// send a reply, to the IP address and port that sent us the packet we just got
	IPAddress destination(192, 168, 1, 2);
	Udp.beginPacket(destination, PORT);
	char msg[30];
	sprintf(msg, "%lu enc1=%ld enc2=%ld ", millis(), encoder1Count, encoder2Count);
	Udp.write(msg, 30);
	Udp.endPacket();
}
