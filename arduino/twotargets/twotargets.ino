#include <Servo.h>

Servo leftTargServo;
Servo rightTargServo;

float leftCommand = 0;
float rightCommand = 0;
int leftServoPin = 5;
int rightServoPin = 6;

int leftFeederPin = 7;
int rightFeederPin = 8;
float leftShoot = false;
float rightShoot = false;
float leftShootOld = false;
float rightShootOld = false;


unsigned long shootMillis = 1000000;
unsigned long lastShootMillis = 0;

void setup() {
  Serial.begin(115200);
  leftTargServo.attach(leftServoPin);
  rightTargServo.attach(rightServoPin);
  pinMode(leftFeederPin,OUTPUT);
  pinMode(rightFeederPin,OUTPUT);
}

void loop()
{
  

  
  while (Serial.available())
  {
    char myChar = Serial.read();
    if (myChar == '!')
    {
      leftCommand = Serial.parseFloat();
      rightCommand = Serial.parseFloat();
      leftShoot = bool(Serial.parseFloat());
      rightShoot = bool(Serial.parseFloat());
//      Serial.print(leftCommand);
//      Serial.print("\t");
//      Serial.print(rightCommand);
//      Serial.print("\t");
//      Serial.print(rightShoot&&!rightShootOld);
//      Serial.print("\t");
//      Serial.print(rightShoot&&!rightShootOld);
//      Serial.print("\t");
//      Serial.print(shootMillis);
//      Serial.println();
      
    }
    else{
      //char junk = Serial.read();
    }
  }

  if((leftShoot&&!leftShootOld)||(rightShoot&&!rightShootOld)){
    lastShootMillis = millis();
  }
  shootMillis = millis()-lastShootMillis ;
  
    leftTargServo.write(int(leftCommand));
    rightTargServo.write(int(rightCommand));
    digitalWrite(leftFeederPin,leftShoot&&(shootMillis<4000)&&(shootMillis>3000));
    digitalWrite(rightFeederPin,rightShoot&&(shootMillis<4000)&&(shootMillis>3000));
    leftShootOld = leftShoot;
    rightShootOld = rightShoot;
    
    
  
  delay(1);

}
