/* <a href="https://nurdspace.nl/ESP8266" rel="nofollow">  https://nurdspace.nl/ESP8266

</a>//http://www.instructables.com/id/Using-the-ESP8266-module/
//https://www.zybuluo.com/kfihihc/note/31135
//http://tminusarduino.blogspot.nl/2014/09/experimenting-with-esp8266-5-wifi-module.html
//http://www.cse.dmu.ac.uk/~sexton/ESP8266/
//https://github.com/aabella/ESP8266-Arduino-library/blob/master/ESP8266abella/ESP8266aabella.h
//http://contractorwolf.com/esp8266-wifi-arduino-micro/
//**********************************************************/


/******************

  SEMI-FONCTIONNEL

******************/

#include <Servo.h>
#include <SoftwareSerial.h>


#define C_TEMP A0
#define C_POID A1
#define C_HUMID A2
#define C_NIVEAU A3

#define DEBUG true //comment out to remove debug msgs

#define _baudrate 115200


#define _SSID ("8Fablab")
#define _PASS ("8fablabdrome")
#define IP "52.200.157.52" // ThingSpeak IP Address: 184.106.153.149

//pin device
#define BOUTTON 52
#define PIN_SERVO 8
#define PIN_LED_RECOLTE 50
#define PIN_LED_NIVEAU 51
#define PIN_LED_POID 48

#define SERVO_INIT 111
#define SERVO_D 75
#define SERVO_G 120

//Variables
String GET = "GET /update?api_key=2HS1MEYTDWZBB2BY";
String chaineRecue="";
int v_temp;
int v_poid;
int v_humid;



Servo servo_recolte;



/*********************

      THINGSPEAK

*********************/


//----- update the  Thingspeak string with 3 values
void updateTS( String T, String P , String H)
{
  // ESP8266 Client
  String cmd = "AT+CIPSTART=\"TCP\",\"";// Setup TCP connection
  cmd += IP;
  cmd += "\",80";//port
  sendDebug(cmd);
  delay(2000);
  

//  cmd = GET + "&field1=" + T + " HTTP/1.0\n\n"; //une seule data
  cmd = GET + "&field1=" + T +"&field2="+ P + "&field3=" + H +" HTTP/1.0\n\n";    //GET /update?api_key=2HS1MEYTDWZBB2BY
  Serial1.print( "AT+CIPSEND=" );
  Serial1.println( cmd.length() );
  if(Serial1.find( ">" ) )
  {
    Serial.print(">");
    Serial.print(cmd);
    Serial1.print(cmd);
  }
  else
  {
    sendDebug("AT+CIPCLOSE");//close TCP connection
  }
  if( Serial1.find("OK") )
  {
    Serial.println( "RECEIVED: OK" );
  }
  else
  {
    Serial.println( "RECEIVED: Error\nExit2" );
  }
}

/*
void get_data()
{
  String cmd2 = "GET /channels/204207/feeds.json?results=1 HTTP/1.0\r\n"; //
  //cmd2+="Host: api.thingspeak.com\n";
  //cmd2+="Connection: close\n";
  cmd2+="Content-type: application/json\r\n\n";
                                                                          //String cmd2 = "GET /channels/204207/feeds.json?results=2 HTTP/1.0\n\n";   //GET /channels/204207/feeds.json?results=2
  
  Serial1.print( "AT+CIPSEND=" );
  
  Serial1.println(cmd2.length());

  Serial.print("-->");
  Serial.print(cmd2);
  Serial.println("<--");
  delay(20);
  Serial1.print(cmd2);


  char c;
  
  while(Serial1.available()==0);
  while(Serial1.available()>0)
  {
    c=Serial1.read();
    Serial.print(c);
    Serial.flush();
  }
  
  Serial.println();
  
}*/

/*********************

         FCT

*********************/



void sendDebug(String cmd)
{
  Serial.print("SEND: ");
  Serial.println(cmd);
  Serial1.println(cmd);
}



String sendData(String command, const int timeout)
{
    String response = "";
    
    Serial1.print(command); // send the read character to the esp8266
    
    long int time = millis();
    
    while( (time+timeout) > millis())
    {
      while(Serial1.available())
      {
        
        // The esp has data so display its output to the serial window 
        char c = Serial1.read(); // read the next character.
        response+=c;
      }  
    }
    
    if(DEBUG)
    {
      Serial.print(response);
      delay(100);
    }
    
    return response;
}


/*********************

        SETUP

*********************/


void setup()
{
  Serial1.begin( _baudrate );
  Serial.begin( _baudrate );

  pinMode(BOUTTON, INPUT);


  /**************PERSO**************/
  
  sendData("AT+RST\r\n",2000); // restart module
  sendData("AT+CWMODE=1\r\n",1000); // 1 pour station, 2 pour point d'accès et 3 pour les deux

  /*String cmd="AT+CWJAP=\""; // Join accespoint
  cmd+=_SSID;
  cmd+="\",\"";
  cmd+=_PASS;
  cmd+="\"";*/
  
  //delay(5000); 
  sendData("AT+CIFSR\r\n",1000); // affiche la ou les IPs sur la liaison serie

  servo_recolte.attach(PIN_SERVO);
  servo_recolte.write(SERVO_INIT);
  

}

/*********************

        LOOP

*********************/



void loop()
{
  v_temp = analogRead(C_TEMP);
  v_poid = analogRead(C_POID);
  v_humid = analogRead(C_HUMID);
  
  
  
  String temp = String(v_temp);// turn integer to string ----  String temp =String(value_temp);
  String poid = String(v_poid);// turn integer to string ---- String light= String(value_light);
  String humid = String(v_humid);// turn integer to string ---- String humid=String(value_humid);
  
  
  if(DEBUG)
  {
    Serial.print("temperature="); Serial.println(temp);
    Serial.print("poid="); Serial.println(poid);
    Serial.print("humidité="); Serial.println(humid);
  }
  
  updateTS(temp, poid, humid);
  delay(1000);
  int i=0;

  //declenchement
  if(digitalRead(BOUTTON)==HIGH)
  {
    digitalWrite(PIN_LED_RECOLTE, HIGH);
    delay(1000);
    servo_recolte.write(SERVO_G);
    delay(3000);
  }
  servo_recolte.write(SERVO_INIT);
  digitalWrite(PIN_LED_RECOLTE, LOW);


  //niveau
  if(analogRead(C_NIVEAU)>100)
  {
    digitalWrite(PIN_LED_NIVEAU,HIGH); 
  }
  else
  {
    digitalWrite(PIN_LED_NIVEAU,LOW); 
  }

  //poid
  if(analogRead(C_POID)<800)
  {
    digitalWrite(PIN_LED_POID,HIGH); 
  }
  else
  {
    digitalWrite(PIN_LED_POID,LOW); 
  }
}




