#include <Servo.h>

Servo leftTargServo;
Servo rightTargServo;

float leftCommand = 0;
float rightCommand = 0;
int leftServoPin = 9;
int rightServoPin = 11;

int leftFeederPin = 4;
int rightFeederPin = 5;

void setup() {
  Serial.begin(115200);
  leftTargServo.attach(9);
  rightTargServo.attach(11);
  pinMode(leftFeederPin,OUTPUT);
  pinMode(rightFeederPin,OUTPUT);
}

void loop()
{
  

  
  if (Serial.available())
  {
    char myChar = Serial.read();
    if (myChar == '!')
    {
      leftCommand = Serial.parseFloat();
      rightCommand = Serial.parseFloat();
      leftShoot = Serial.parseFloat();
      rightShoot = Serial.parseFloat();
      
    }
    else{
      //char junk = Serial.read();
    }
  }
    leftTargServo.write(int(leftCommand));
    rightTargServo.write(int(rightCommand));
    digitalWrite(leftFeederPin,bool(leftShoot));
    digitalWrite(rightFeederPin,bool(rightShoot));

  delay(1);

}
