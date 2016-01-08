#include <Servo.h>
#include <SPI.h>
#include <EthernetV2_0.h>
#include <EthernetUdpV2_0.h>

const int LEFT_MOTOR_PWM_PIN = 5;
const int RIGHT_MOTOR_PWM_PIN = 6;

Servo leftMotor;
Servo rightMotor;

// server stuff
boolean lastConnected = false;
String currentLine;
byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0xD4, 0xE7 };
IPAddress myIP;
IPAddress ip(192, 162, 1, 177);

// set point
EthernetUdp setPointClient;

void setup() {
	// put your setup code here, to run once:

	pinMode(LEFT_MOTOR_PWM_PIN, OUTPUT);
	pinMode(RIGHT_MOTOR_PWM_PIN, OUTPUT);

	leftMotor.attach(LEFT_MOTOR_PWM_PIN);
	rightMotor.attach(RIGHT_MOTOR_PWM_PIN);

	//get our ip address
	myIP = Ethernet.localIP();

	//print the local IP address:
	Serial.print("My IP address: ");
	for (byte thisByte = 0; thisByte < 4; thisByte++) {
	  // print the value of each byte of the IP address:
	  Serial.print(myIP[thisByte], DEC);
	  Serial.print(".");
	}
	Serial.println();

	Serial.println("Done with setup()!");
}

void loop() {
	// put your main code here, to run repeatedly:

	for (int i = -10; i < 10; i += 1) {
		Serial.print("Writing ");
		Serial.print(i);
		Serial.println(" to the left servo.");
		setSpeed(&leftMotor, i, 1);

		Serial.print("Writing ");
		Serial.print(i);
		Serial.println(" to the right servo.");
		setSpeed(&rightMotor, i, -1);
		
		delay(2000);
	}

	// uncomment this to calibrate the servo'
	// setSpeed(&rightMotor, 0, -1);
	// setSpeed(&leftMotor, 0, 1);

}

void setSpeed(Servo *servo, int speed, int flip) {
	servo->writeMicroseconds(flip * 2 * speed + 1500);
}