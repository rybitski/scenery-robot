/*
This program is able to constantly read commands from an
xbox controller. It immediately turns the motors according
to those values. While it's turning, it's also recording the
encoder ticks generated by these turns.
*/

#include <Servo.h>
#include <SPI.h>
#include <EthernetV2_0.h>

const int SDCARD_CS_PIN = 4;

Servo leftMotor;
Servo rightMotor;

// Slave Select pins for encoders 1 and 2
// Feel free to reallocate these pins to best suit your circuit
const int slaveSelectEnc1 = 7;
const int slaveSelectEnc2 = 8;

// These hold the current encoder count.
signed long encoder1count = 0;
signed long encoder2count = 0;

// server stuff
boolean lastConnected = false;
String currentLine;
byte mac[] = { 0x62, 0x02, 0x69, 0x9E, 0xC4, 0xFF };
const int PORT = 29281;
IPAddress ip(192, 168, 1, 3);
EthernetClient client;

// datastructure to hold the path
// Only 16 long because of memorize size constraints
// Longs are 4 bytes, * 2 * 16 = 1024 bytes
// SuperDroid Robots Dual LS7366R Quadrature Encoder Buffer
const int BUFFER_SIZE = 16;
signed long pathBuffer[BUFFER_SIZE][2]; // for left and right encoder
unsigned int pathBufferIndex = 0;

const byte HEADER_BYTE = 0xA5;
// datastructure to hold the controls from the server
typedef struct {
	byte leftMotorPower; // between -127 and 127, to match Sabertooth controller
	byte rightMotorPower; // between -127 and 127, to match Sabertooth controller
	// byte deadManSwitch; // code to enable motors
} Controls;
Controls controls; // specific instance of struct

typedef enum {header, left, right} ReceiveState;
ReceiveState receiveState;

void initEncoders() {
	// Set slave selects as outputs
		pinMode(slaveSelectEnc1, OUTPUT);
		pinMode(slaveSelectEnc2, OUTPUT);

	// Raise select pins
	// Communication begins when you drop the individual select signsl
		digitalWrite(slaveSelectEnc1,HIGH);
		digitalWrite(slaveSelectEnc2,HIGH);

		SPI.begin();

	// Initialize encoder 1
	//    Clock division factor: 0
	//    Negative index input
	//    free-running count mode
	//    x4 quatrature count mode (four counts per quadrature cycle)
	// NOTE: For more information on commands, see datasheet
	digitalWrite(slaveSelectEnc1,LOW);        // Begin SPI conversation
	SPI.transfer(0x88);                       // Write to MDR0
	SPI.transfer(0x03);                       // Configure to 4 byte mode
	digitalWrite(slaveSelectEnc1,HIGH);       // Terminate SPI conversation 

	// Initialize encoder 2
	//    Clock division factor: 0
	//    Negative index input
	//    free-running count mode
	//    x4 quatrature count mode (four counts per quadrature cycle)
	// NOTE: For more information on commands, see datasheet
	digitalWrite(slaveSelectEnc2,LOW);        // Begin SPI conversation
	SPI.transfer(0x88);                       // Write to MDR0
	SPI.transfer(0x03);                       // Configure to 4 byte mode
	digitalWrite(slaveSelectEnc2,HIGH);       // Terminate SPI conversation 
}

long readEncoder(int encoder) {

	// Initialize temporary variables for SPI read
	unsigned int count_1, count_2, count_3, count_4;
	long count_value;  

	// Read encoder 1
	if (encoder == 1) {
		digitalWrite(slaveSelectEnc1,LOW);      // Begin SPI conversation
		SPI.transfer(0x60);                     // Request count
		count_1 = SPI.transfer(0x00);           // Read highest order byte
		count_2 = SPI.transfer(0x00);           
		count_3 = SPI.transfer(0x00);           
		count_4 = SPI.transfer(0x00);           // Read lowest order byte
		digitalWrite(slaveSelectEnc1,HIGH);     // Terminate SPI conversation 
	}

	// Read encoder 2
	else if (encoder == 2) {
		digitalWrite(slaveSelectEnc2,LOW);      // Begin SPI conversation
		SPI.transfer(0x60);                      // Request count
		count_1 = SPI.transfer(0x00);           // Read highest order byte
		count_2 = SPI.transfer(0x00);           
		count_3 = SPI.transfer(0x00);           
		count_4 = SPI.transfer(0x00);           // Read lowest order byte
		digitalWrite(slaveSelectEnc2,HIGH);     // Terminate SPI conversation 
	}

	// Calculate encoder count
	count_value = (count_1 << 8) + count_2;
	count_value = (count_value << 8) + count_3;
	count_value = (count_value << 8) + count_4;

	return count_value;
}

void clearEncoderCount() {
	// Set encoder1's data register to 0
	digitalWrite(slaveSelectEnc1,LOW);      // Begin SPI conversation  
	// Write to DTR
	SPI.transfer(0x98);    
	// Load data
	SPI.transfer(0x00);  // Highest order byte
	SPI.transfer(0x00);           
	SPI.transfer(0x00);           
	SPI.transfer(0x00);  // lowest order byte
	digitalWrite(slaveSelectEnc1,HIGH);     // Terminate SPI conversation 

	delayMicroseconds(100);  // provides some breathing room between SPI conversations

	// Set encoder1's current data register to center
	digitalWrite(slaveSelectEnc1,LOW);      // Begin SPI conversation  
	SPI.transfer(0xE0);    
	digitalWrite(slaveSelectEnc1,HIGH);     // Terminate SPI conversation   

	// Set encoder2's data register to 0
	digitalWrite(slaveSelectEnc2,LOW);      // Begin SPI conversation  
	// Write to DTR
	SPI.transfer(0x98);    
	// Load data
	SPI.transfer(0x00);  // Highest order byte
	SPI.transfer(0x00);           
	SPI.transfer(0x00);           
	SPI.transfer(0x00);  // lowest order byte
	digitalWrite(slaveSelectEnc2,HIGH);     // Terminate SPI conversation 

	delayMicroseconds(100);  // provides some breathing room between SPI conversations

	// Set encoder2's current data register to center
	digitalWrite(slaveSelectEnc2,LOW);      // Begin SPI conversation  
	SPI.transfer(0xE0);    
	digitalWrite(slaveSelectEnc2,HIGH);     // Terminate SPI conversation 
}

void setup() {
	Serial.begin(9600);

	Serial.println("Begin setup()");
	Serial.println("We are the client!");

	initEncoders();       Serial.println("Encoders Initialized...");  
	clearEncoderCount();  Serial.println("Encoders Cleared...");

	// Set chip select high (inactive) for SD card.
	pinMode(SDCARD_CS_PIN, OUTPUT);
	digitalWrite(SDCARD_CS_PIN, HIGH);

	Serial.print("Configuring Ethernet client using static IP... ");
	Ethernet.begin(mac, ip);
	Serial.print("Success. ");

	delay(1000); // give the Ethernet sheild a second to initialize

	// get and print our IP address
	Serial.print("(Our IP: ");
	Serial.print(Ethernet.localIP());
	Serial.println(")");
	Serial.println();

	char serverName[] = "192.168.1.2";
	Serial.print("Trying to connect to server at ");
	Serial.print(serverName);
	Serial.print("... ");
	if (client.connect(serverName, PORT)) {
		Serial.println("connected.");
		client.print("Hi!!! My name is ");
		client.print(Ethernet.localIP());
		client.println(". Thx for letting me connect!");
		client.println();
	}
	else {
		Serial.println("failed.");
	}

	Serial.println("Done with setup()");
}

void parseByteFromServer(byte b) {
	// switch on state
	switch (receiveState) {
		case header:
			if (b == HEADER_BYTE) {
				receiveState = left;
			}
			break;
		case left:
			controls.leftMotorPower = b;
			receiveState = right;
			break;
		case right:
			controls.rightMotorPower = b;
			receiveState = header;
			break;
		default:
			;
			break;
	}
}

void loop() {

	// Retrieve current encoder counters
	encoder1count = readEncoder(1); 
	encoder2count = readEncoder(2);

	Serial.print("Enc1: ");
	Serial.print(encoder1count);
	Serial.print(" Enc2: ");
	Serial.print(encoder2count); 

	Serial.print(" leftMotorPower: ");
	Serial.print(controls.leftMotorPower);
	Serial.print(" rightMotorPower: ");
	Serial.println(controls.rightMotorPower);

	// if there are incoming bytes available 
	// from the server, read them and print them:
	if (client.available()) {
		byte c = client.read();
		parseByteFromServer(c);
	}

	// send the recorded path buffer back to the server
	// client.write(pathBuffer[pathBufferIndex], 2);
	// if (++pathBufferIndex == BUFFER_SIZE) {
	// 	pathBufferIndex = 0;
	// }
	const char message[] = {'B', '\n'};
	client.write(encoder1count);

	// if the server's disconnected, stop the client:
	if (!client.connected()) {
		Serial.println();
		Serial.println("Server has disconnected. Stopping client.");
		client.stop();

		// do nothing forevermore:
		while(true);
	}
}
