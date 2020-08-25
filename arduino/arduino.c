const int LED = 8;
const int MOTOR = 10;
byte buffer[2];

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(MOTOR, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() >= 2) {
	for (int i = 0; i < 3; i++) {
	  buffer[i] = Serial.read();
	}
	if (buffer[0] == 1) {
	  digitalWrite(LED, 1);
	}
	else if(buffer[0] == 2) {
	  digitalWrite(LED, 0);
	}
	else if (buffer[0] == 3) {
	  setMotorSpeed((int)buffer[1]);
	}
  }

}

void setMotorSpeed(int speed) {
  speed = constrain(speed, 0, 255);
  analogWrite(MOTOR, speed);
}