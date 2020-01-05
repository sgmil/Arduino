#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

    // Reserve memory space for your JSON data
  StaticJsonBuffer<200> jsonBuffer;
  
  // Build your own object tree in memory to store the data you want to send in the request
  JsonObject& root = jsonBuffer.createObject();
  root["sensor"] = "dht11";
  
  JsonObject& data = root.createNestedObject("data");
  data.set("temperature", "30.1");
  data.set("humidity", "70.1");
  
  // Generate the JSON string
  root.printTo(Serial);
  
  Serial.print("POST ");
  Serial.println(resource);

  client.print("POST ");
  client.print("/json-post");
  client.println(" HTTP/1.1");
  client.print("Host: ");
  client.println("127.0.0.1:5000");
  client.println("Connection: close\r\nContent-Type: application/json");
  client.print("Content-Length: ");
  client.print(root.measureLength());
  client.print("\r\n");
  client.println();
  root.printTo(client);
