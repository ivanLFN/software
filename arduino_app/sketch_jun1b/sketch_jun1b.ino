#include <Wire.h>
#include <Adafruit_LSM303.h>

Adafruit_LSM303 lsm;

void setup() {
  Wire.begin();
  Serial.begin(9600);

  if (!lsm.begin()) {
    Serial.println("Не найдено LSM303DLHC!");
    while (1);
  }
}

void loop() {
  if (Serial.available() > 0) {
    byte command = Serial.read();
    byte pin1 = Serial.read();
    byte pin2 = Serial.read();
    int stepCount = Serial.parseInt();
    int dir = Serial.parseInt();

    if (command == 'r') {
      Moving(pin1, pin2, stepCount, dir);
    }

    if (command == 'g') {
      int16_t gyro_x, gyro_y, gyro_z;
      float accel_x, accel_y, accel_z;

      lsm.read();
      gyro_x = lsm.gyroData.x;
      gyro_y = lsm.gyroData.y;
      gyro_z = lsm.gyroData.z;

      accel_x = lsm.accelData.x;
      accel_y = lsm.accelData.y;
      accel_z = lsm.accelData.z;

      Serial.print(accel_x);
      Serial.print(",");
      Serial.print(accel_y);
      Serial.print(",");
      Serial.print(accel_z);
      Serial.print(",");

      Serial.print(gyro_x);
      Serial.print(",");
      Serial.print(gyro_y);
      Serial.print(",");
      Serial.println(gyro_z);
    }
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