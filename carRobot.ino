
#define I1 8  // Control pin 1 for motor 1
#define I2 9  // Control pin 2 for motor 1
#define I3 11 // Control pin 1 for motor 2
#define I4 12  // Control pin 2 for  motor 2
#include <SoftwareSerial.h>
SoftwareSerial BTSerial(3,4);
char data = 0;    
const int trigPin = 5;
const int echoPin = 6;
// defines variables
long duration;
int distance;
int count=0;
void setup() {
    Serial.begin(9600);   //Sets the baud for serial data transmission                               
    BTSerial.begin(38400);
    pinMode(I1, OUTPUT);
    pinMode(I2, OUTPUT);
    pinMode(I3, OUTPUT);
    pinMode(I4, OUTPUT);
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
}
 void backward(){
    digitalWrite(I1, HIGH);
    digitalWrite(I2, LOW);
   digitalWrite(I3, HIGH);
   digitalWrite(I4, LOW);
 }

 void forward(){
   digitalWrite(I1, LOW);
  digitalWrite(I2, HIGH);
    digitalWrite(I3, LOW);
    digitalWrite(I4, HIGH);
 }

  void right(){
   digitalWrite(I1, HIGH);
   digitalWrite(I2, LOW);
    digitalWrite(I3, HIGH);
    digitalWrite(I4, HIGH);
 }

  void left(){
   digitalWrite(I1, HIGH);
   digitalWrite(I2, HIGH);
    digitalWrite(I3, HIGH);
    digitalWrite(I4, LOW);
 }

 void Stop(){
   digitalWrite(I1, HIGH);
   digitalWrite(I2, HIGH);
    digitalWrite(I3, HIGH);
    digitalWrite(I4, HIGH);
  }
void Search(){
  right();
}
void loop() {
  digitalWrite(trigPin, LOW);
delayMicroseconds(2);
// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echoPin, HIGH);
// Calculating the distance
distance= duration*0.034/2;
// Prints the distance on the Serial Monitor
Serial.print("Distance: ");
Serial.println(distance);
if(distance<25)
 {
  count++;
  Serial.println("rukh ");
 }
 if(count>=5){
  Stop();
  count=0;
  delay(1000);
  backward();
  delay(3000);
  Stop();
 }
  while (BTSerial.available()) {
      data = BTSerial.read();
      Serial.println(data);
     
      if(data=='f' || data=='F'){
//        Serial.println("Forward");
        forward();
        
      }
      else if(data=='b' || data=='B'){
        backward();
       
      }
      else if(data=="r" || data=='R'){
        right();
        
      }
      else if(data=='l' || data=='L'){
        left();
        
      }
      else if(data=='s' || data=='S'){
        Stop();
        
      }
      else if(data=='x' || data=='X' && sear<10){
        Search();
        sear++;
        delay(1000);
        Stop();
      }
     
    }
}

