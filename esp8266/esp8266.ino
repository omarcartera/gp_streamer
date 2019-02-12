#include <ESP8266WiFi.h>    // The Basic Function Of The ESP NOD MCU
//------------------------------------------------------------------------------------
// WIFI Authentication Variables
//------------------------------------------------------------------------------------
/* This Client Is Going To Connect To A WIFI Server Access Point
 * So You Have To Specify Server WIFI SSID & Password In The Code Not Here
 * Please See The Function Below Name (WiFi.Begin)
 * If WIFI dont need Any password Then WiFi.begin("SSIDNAME")
 * If WIFI needs a Password Then WiFi.begin("SSIDNAME", "PASSWORD")
 */
char*         TKDssid;            // Wifi Name
char*         TKDpassword;        // Wifi Password
//------------------------------------------------------------------------------------
// WIFI Module Role & Port
//------------------------------------------------------------------------------------
/* This WIFI Module Code Works As A Client
 * That Will Connect To A Server WIFI Modul With (IP ADDress 192.168.4.1)
 */
int             TKDServerPort  = 5557;
IPAddress       TKDServer(192,168,1,14);
WiFiClient      TKDClient;

int counter = 0;
char dir = 0;

void setup() 
{
  // Setting The Serial Port
  Serial.begin(115200);           // Computer Communication

  // Starting To Connect
  if(WiFi.status() == WL_CONNECTED)
  {
    WiFi.disconnect();
    WiFi.mode(WIFI_OFF);
    delay(50);
  }

  /* in this part it should load the ssid and password 
   * from eeprom they try to connect using them */
  
  WiFi.mode(WIFI_STA);            // To Avoid Broadcasting An SSID
  WiFi.begin("RUN", "0T64E3[886Z29Em");      // The SSID That We Want To Connect To

  // Printing Message For User That Connetion Is On Process ---------------
  Serial.println("!--- Connecting To " + WiFi.SSID() + " ---!");

  // WiFi Connectivity ----------------------------------------------------
  CheckWiFiConnectivity();        // Checking For Connection

  Serial.println("!-- Client Device Connected --!");

  // Printing IP Address --------------------------------------------------
  Serial.println("Connected To      : " + String(WiFi.SSID()));
  Serial.println("Signal Strenght   : " + String(WiFi.RSSI()) + " dBm");
  Serial.print  ("Server IP Address : ");
  Serial.println(TKDServer);
  Serial.print  ("Server Port Num   : ");
  Serial.println(TKDServerPort);
  // Printing MAC Address
  Serial.print  ("Device MC Address : ");
  Serial.println(String(WiFi.macAddress()));
  // Printing IP Address
  Serial.print  ("Device IP Address : ");
  Serial.println(WiFi.localIP());
  
  // Conecting The Device As A Client -------------------------------------
  TKDRequest();
}

  
void loop()
{
  delay(5);

  if(dir == 0)
  {
    counter += 4;
  }

  else
  {
    counter -= 4;
  }

  if(counter >= 10)
  {
    dir = 1;
  }

  else if(counter <= -10)
  {
    dir = 0;
  }

  //ReadButton();
  
  TKDClient.print(int(analogRead(A0)));
  TKDClient.flush();
}


void CheckWiFiConnectivity()
{
  while(WiFi.status() != WL_CONNECTED)
  {
    for(int i=0; i < 10; i++)
    {
      delay(250);
      Serial.print(".");
    }
    Serial.println("");
  }
}


void TKDRequest()
{
  // First Make Sure You Got Disconnected
  TKDClient.stop();

  // If Sucessfully Connected Send Connection Message
  if(TKDClient.connect(TKDServer, TKDServerPort))
  {
    Serial.println    ("<-CONNECTED>");
    //TKDClient.println ("<-CONNECTED>");
  }
}
