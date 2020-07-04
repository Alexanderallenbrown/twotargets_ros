#include <Servo.h>

Servo leftTargServo;
Servo rightTargServo;

float leftCommand = 0;
float rightCommand = 0;
int leftServoPin = 44;
int rightServoPin = 46;

int leftFeederPin = 4;
int rightFeederPin = 5;
float leftShoot = false;
float rightShoot = false;

void setup() {
  Serial.begin(115200);
  leftTargServo.attach(leftServoPin);
  rightTargServo.attach(rightServoPin);
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
      Serial.print(leftCommand);
      Serial.print("\t");
      Serial.print(rightCommand);
      Serial.print("\t");
      Serial.print(bool(leftShoot));
      Serial.print("\t");
      Serial.print(bool(rightShoot));
      Serial.println();
      
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
