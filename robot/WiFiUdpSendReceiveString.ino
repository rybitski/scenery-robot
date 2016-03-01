
#include <SPI.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <Sabertooth.h>


// ----- WIFI -----
int status = WL_IDLE_STATUS;
char ssid[] = ""; //  your network SSID (name) 
char pass[] = "";    // your network password (use for WPA, or use as key for WEP)

// ----- UDP -----
WiFiUDP Udp;
const unsigned int UDP_PORT = 5500;      // local port to listen on
char packetBuffer[255]; //buffer to hold incoming packet
char  ReplyBuffer[] = "acknowledged";       // a string to send back

// ----- SABERTOOTH -----
Sabertooth ST(128); // Address 128, use pin 1 as hardware TX - Edison does not support software serial

// ----- MOTORS -----
int8_t leftMotorSpeed; // between -127 and 127, to match Sabertooth controller
int8_t rightMotorSpeed; // between -127 and 127, to match Sabertooth controller

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  SabertoothTXPinSerial.begin(9600);
  ST.autobaud();
  
  // attempt to connect to Wifi network:
  while ( status != WL_CONNECTED) { 
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:    
    status = WiFi.begin(ssid, pass);
  
    // wait 10 seconds for connection:
    delay(10000);
  } 
  Serial.println("Connected to wifi");
  printWifiStatus();
  
  Serial.println("\nStarting connection to server...");
  
  // if you get a connection, report back via serial:
  Udp.begin(UDP_PORT);  
}

void loop() {
    
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if(packetSize)
  {   
    // read the packet into packetBufffer
    int len = Udp.read(packetBuffer,12);
    if (len >0) packetBuffer[len]=0;
    //Serial.println("Contents:");
    //Serial.println(packetBuffer);

    // Copy contents of packet into variables
    memcpy(&leftMotorSpeed, &packetBuffer[4], 1);
    memcpy(&rightMotorSpeed, &packetBuffer[5], 1);
  }

  ST.motor(1, leftMotorSpeed);
  ST.motor(2, rightMotorSpeed);
}


void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}




