// region Pin allocation
const int motorOneForward = 11;
const int motorOneReverse = 10;
const int motorTwoForward = 6;
const int motorTwoReverse = 5;
// endregion


int motors[][2] = {{motorOneForward, motorOneReverse}, {motorTwoForward, motorTwoReverse}};
int motorStates[] = {"forward", "reverse", "stop"};
String movementSequence = "fblrffff";
int movementCounter = 0;

void moveForward(int units, int power=50); // power as percentage from 0 to 100
void moveBackward(int units, int power=50); // power as percentage from 0 to 100
void rotateLeft(int degs=90, int power=50); // power as percentage from 0 to 100
void rotateRight(int degs=90, int power=50); // power as percentage from 0 to 100
void stopMotion(int delayTime=20);


void setup() {
  pinMode(motorOneForward, OUTPUT);
  pinMode(motorOneReverse, OUTPUT);
  pinMode(motorTwoForward, OUTPUT);
  pinMode(motorTwoReverse, OUTPUT);
  Serial.begin(9600);
  Serial.println("\n\n\n\nRunning...");

}

void loop() {
  delay(1000);
  String command = "";
  if (movementCounter >= 0 and movementCounter < movementSequence.length()) {
    command = movementSequence[movementCounter++];
  }
  if(Serial.available()){
      Serial.println("Reading serial...");
      command = Serial.readString();
//    Serial.println(command.length());
//    command = command.substring(0, command.length() - 1);
//    Serial.println(command.length());
      command = command[0];
  }
  if(command == "f"){
    moveForward(1);
    Serial.println("forward");
  } else if (command == "b"){
    moveBackward(1);
    Serial.println("reverse");
  } else if (command == "l") {
    rotateLeft();
    Serial.println("left");
  } else if (command == "r") {
    rotateRight();
    Serial.println("right");
  } else {
    changeMotorState(0, "stop");
    changeMotorState(1, "stop");
  }

}

void moveForward(int units, int power){
  power = power * 255 / 100;
  stopMotion(20);
  analogWrite(motorOneForward, power);
  analogWrite(motorOneReverse, 0);
  analogWrite(motorTwoForward, power);
  analogWrite(motorTwoReverse, 0);
  delay(300);
  stopMotion(0);
}

void moveBackward(int units, int power){
  power = power * 255 / 100;
  stopMotion(20);
  analogWrite(motorOneForward, 0);
  analogWrite(motorOneReverse, power);
  analogWrite(motorTwoForward, 0);
  analogWrite(motorTwoReverse, power);
  delay(300);
  stopMotion(0);
}


void rotateLeft(int degs, int power){ // use degrees as input i.e. 90, 180, 270, 360 for quarter turns
  power = power * 255 / 100;
  stopMotion(20);
  analogWrite(motorOneForward, power);
  analogWrite(motorOneReverse, 0);
  analogWrite(motorTwoForward, 0);
  analogWrite(motorTwoReverse, power);
  delay(300);
  stopMotion(0);
}

void rotateRight(int degs, int power){ // use degrees as input i.e. 90, 180, 270, 360 for quarter turns
  // 250 ms at 50% power is an approximate quarter turn
  power = power * 255 / 100;
  stopMotion(20);
  analogWrite(motorOneForward, 0);
  analogWrite(motorOneReverse, power);
  analogWrite(motorTwoForward, power);
  analogWrite(motorTwoReverse, 0);
  delay(300);
  stopMotion(0);
}

void stopMotion(int delayTime){
  analogWrite(motorOneForward, 0);
  analogWrite(motorOneReverse, 0);
  analogWrite(motorTwoForward, 0);
  analogWrite(motorTwoReverse, 0);
  delay(delayTime);
}

void changeMotorState(int motorNumber, String motorState){
  if (motorState.equals("forward")){
    analogWrite(motors[motorNumber][0], 0);
    analogWrite(motors[motorNumber][1], 0);
    delay(20);
    analogWrite(motors[motorNumber][0], 128);
    analogWrite(motors[motorNumber][1], 0);
  } else if (motorState == "reverse"){
    analogWrite(motors[motorNumber][0], 0);
    analogWrite(motors[motorNumber][1], 0);
    delay(20);
    analogWrite(motors[motorNumber][0], 0);
    analogWrite(motors[motorNumber][1], 128);
  } else {
    analogWrite(motors[motorNumber][0], 0);
    analogWrite(motors[motorNumber][1], 0);
    delay(20);
  } 
}
