// {filename} Copyright {date} {developer}
#define BOARD "esp8266:esp8266:nodemcuv2"
#define IP_ADDRESS "192.168.0.177"
#define PORT "/dev/ttyUSB0"
/*
 * Please make appropriate changes to
 * the above defines. Enter board definition,
 * the static IP address to be assigned,
 * and the port where board is attached.
 *
*/
#include "My_ESP8266_Functions.h"
#include <Arduino.h>
#include <string.h>
using namespace std;

static string IP = IP_ADDRESS;


//Function Prototypes//


//Variables//


//Instantiations
MyWiFi wifi("ESP8266",IP);

void setup(void)
{

}

void loop(void)
{

}
