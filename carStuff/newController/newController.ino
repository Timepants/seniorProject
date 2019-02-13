//Motor Connections
#define enA 10
#define enB 9
#define in1 7
#define in2 6
#define in3 5
#define in4 4

int throttle = 0;
int incomingByte = -1;
int lastByte= -1;

void setup()
{
  Serial.begin(9600);
  // set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

}
//byte = f
void goForward(int pThrottle){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA, pThrottle); 
}
//byte = b
void goBackward(int pThrottle){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, pThrottle); 
}
//byte = l
void turnLeft(){
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, 255); 
}
//byte = r
void turnRight(){
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enB, 255); 
}
//byte = s
void clearAll(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);  
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);   
}
//byte = m
void clearMovement(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);    
}
//byte = h
void clearHeading(){
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);   
}
void changeThrottle(int pThrottle){
  analogWrite(enA, pThrottle); 
}
void loop()
{
int seri = Serial.available();
if (seri > 0) {
  incomingByte = Serial.read(); 
  if (incomingByte > 10){
    if(lastByte == 't'){
      Serial.print("I received after t: ");
      Serial.println(incomingByte);
      throttle = incomingByte;
      changeThrottle(throttle);
    } else {
    Serial.print("I received: ");
    char byted = incomingByte;
    Serial.println(byted);
    switch(incomingByte){
      case 's':
        clearAll();
      break;
      case 'm':
        clearMovement();
      break;
      case 'h':
        clearHeading();
      break;
      case 'f':
        goForward(throttle);
      break;
      case 'b':
        goBackward(throttle);
      break;
      case 'l':
        turnLeft();
      break;
      case 'r':
        turnRight();
      break;
    }
    }
  //  Serial.print(HIGH);
  //  demoOne();
  //  delay(1000);
  //  demoTwo();
  //  turnLeft();
  //  goForward(70);
    lastByte = incomingByte;
  }
  } 
}
