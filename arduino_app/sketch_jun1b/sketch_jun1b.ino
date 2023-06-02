void setup() {
  // Same setup code as before
  ...
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming data
    byte pin1 = Serial.read();
    byte pin2 = Serial.read();
    int stepCount = Serial.parseInt();
    int dir = Serial.parseInt();
    
    // Call the Moving function with the received data
    Moving(pin1, pin2, stepCount, dir);
  }
}

void Moving(byte pin1, byte pin2, int stepCount, int dir) {
  digitalWrite(pin1, dir);
  
  for (int x = 0; x < stepCount; x++) {
    digitalWrite(pin2, HIGH);
    delayMicroseconds(400);
    digitalWrite(pin2, LOW);
    delayMicroseconds(400);
  }
}
