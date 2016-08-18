#include <Servo.h>

// Variables
//==========
Servo Motor1;
Servo Motor2; 
int vibration;
int pinMotor1=7;
int pinMotor2=8;
int pinbeeper=4; // haut parleur ou alarme
char info;
byte angle=0;

  

void setup() {

  Serial.begin(115200);
  Motor1.attach(pinMotor1);
  Motor2.attach(pinMotor2);
  Motor2.write(0);
  Motor1.write(0);
  pinMode(pinbeeper, OUTPUT);
}

void loop() {
  // Tout est une question de vitesse de lecture :p
  int sensor= analogRead(A0);
  frappePorte(sensor);
  while (Serial.available() >0){
    info=Serial.read();
    if (info==1){
      delay(5);
      angle=Serial.read();
      Motor1.write(angle);
    }
    if (info==2){
      delay(5);
      angle=Serial.read();
      Motor2.write(angle);
    }
    if (info==3){
      beep(pinbeeper,1000);
    }
  }
  
}
int frappePorte(int sensor){
     if (sensor >1000){
    vibration=1;
    Serial.println("porte");
   }
  

}

void beep(int pin, int dureTonalite){
  // Alarme avec dureTonalite= temps de la sonnerie
  float periode=1/4*1000*1000;
  long int startTime=millis();
  while(millis()-startTime <dureTonalite){
    digitalWrite(pin, HIGH);
    delayMicroseconds(periode/2);
    digitalWrite(pin,LOW);
    delayMicroseconds(periode/2);
  }
  
}


