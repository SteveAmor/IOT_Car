/*
Intranet of Things Car Client
 */

#define BUZZER_PIN 0

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid     = "xxxxxx";
const char* password = "xxxxxx";

ESP8266WebServer server ( 80 );

IPAddress ip(192,168,0,1);
IPAddress gateway(192,168,0,254);
IPAddress subnet(255,255,255,0);

void beep(int times) {
  for( ; times>0; times--) {
    digitalWrite(BUZZER_PIN, LOW);
    delay(200);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
  }
}

void handleRoot() {
    char temp[10];
    int sec = millis() / 1000;
    snprintf ( temp, 10, "%d", sec);
    server.send ( 200, "text/html", temp );
}

void handleBeep1() {
  handleRoot();
  beep(1);  
}

void handleBeep2() {
  handleRoot();
  beep(2);
}

void handleBeep3() {
  handleRoot();
  beep(3);
}

void setup() {

  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, HIGH);

  WiFi.begin(ssid, password);
  WiFi.config(ip, gateway, subnet);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  server.on ( "/", handleRoot);
  server.on ( "/beep1", handleBeep1); 
  server.on ( "/beep2", handleBeep2);
  server.on ( "/beep3", handleBeep3); 
  server.begin();
}


void loop() {
  server.handleClient(); 
}


