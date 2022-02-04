// Test2.ino // Copyright 2022-01-18 Stephen Milhiem
#define BOARD "esp8266:esp8266:nodemcuv2"
#define IP_ADDRESS "192.168.0.177"
#define PORT "/dev/ttyUSB0"
/*
 * Please make appropriate changes to
 * the above defines. Enter board definition,
 * the static IP address to be assigned,
 * and the port where board is attached.
 * These headers are stripped by bash script
 * to provide arguments to arduino-cli.
*/
#define OTAok (BOARD=="esp8266:esp8266:nodemcuv2")

#include <Arduino.h>
#include "My_ESP8266_Functions.h" // set up wifi, thingspeak, OTA upload

//Function Prototypes//

//Variables//
String IP = IP_ADDRESS;
MyWiFi wifi("ESP8266",IP);

void setup(void)
{
    wifi.connectWiFi();
    if (OTAok) wifi.myOTAsetup();      // makes OTA upload possibe
}
void loop(void)
{
    if (OTAok) wifi.myOTAhandle();
}
