// {filename} Copyright {date} {developer}
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
#include "My_ESP8266_Functions.h" // set up wifi, thingspeak, OTA upload
#include <Arduino.h>
#include <string.h>               // to manipulate IP address in My_ESP8266_Functions

using namespace std;
//Function Prototypes//

//Variables//
static string IP = IP_ADDRESS;  // C++ string needed for setting up wifi
MyWiFi wifi("ESP8266",IP);      

void setup(void)
{
    wifi.connectWiFi();
    wifi.myOTAsetup();      // makes OTA upload possibe
}
void loop(void)
{
    wifi.myOTAhandle();
}
