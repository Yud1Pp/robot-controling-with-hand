#include <Servo.h>

Servo indexServo;   // Servo untuk jari telunjuk
Servo middleServo;  // Servo untuk jari tengah
Servo ringServo;    // Servo untuk jari manis
Servo pinkyServo;   // Servo untuk jari kelingking
Servo thumbServo;   // Servo untuk jari jempol

int indexServoPin = 3;
int middleServoPin = 5;
int ringServoPin = 6;
int pinkyServoPin = 7;
int thumbServoPin = 11;  // Pin servo jari jempol

void setup() {
  indexServo.attach(indexServoPin);    // Hubungkan servo jari telunjuk ke pin
  middleServo.attach(middleServoPin);  // Hubungkan servo jari tengah ke pin
  ringServo.attach(ringServoPin);      // Hubungkan servo jari manis ke pin
  pinkyServo.attach(pinkyServoPin);    // Hubungkan servo jari kelingking ke pin
  thumbServo.attach(thumbServoPin);    // Hubungkan servo jari jempol ke pin

  indexServo.write(0);
  middleServo.write(0);
  ringServo.write(0);
  pinkyServo.write(0);
  thumbServo.write(0);
  Serial.begin(9600);  // Memulai komunikasi serial dengan baud rate 9600
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');  // Membaca data dari serial hingga karakter newline ('\n')
    int firstCommaIndex = data.indexOf(',');
    int secondCommaIndex = data.indexOf(',', firstCommaIndex + 1);
    int thirdCommaIndex = data.indexOf(',', secondCommaIndex + 1);
    int fourthCommaIndex = data.indexOf(',', thirdCommaIndex + 1);

    if (firstCommaIndex > 0 && secondCommaIndex > 0 && thirdCommaIndex > 0 && fourthCommaIndex > 0) {
      String indexAngleStr = data.substring(0, firstCommaIndex);
      String middleAngleStr = data.substring(firstCommaIndex + 1, secondCommaIndex);
      String ringAngleStr = data.substring(secondCommaIndex + 1, thirdCommaIndex);
      String pinkyAngleStr = data.substring(thirdCommaIndex + 1, fourthCommaIndex);
      String thumbAngleStr = data.substring(fourthCommaIndex + 1);

      int indexAngle = indexAngleStr.toInt();    // Konversi string sudut telunjuk menjadi integer
      int middleAngle = middleAngleStr.toInt();  // Konversi string sudut tengah menjadi integer
      int ringAngle = ringAngleStr.toInt();      // Konversi string sudut manis menjadi integer
      int pinkyAngle = pinkyAngleStr.toInt();    // Konversi string sudut kelingking menjadi integer
      int thumbAngle = thumbAngleStr.toInt();    // Konversi string sudut jempol menjadi integer

      // Konstrain sudut antara 0 hingga 180 derajat untuk memastikan sudut valid
      indexAngle = constrain(indexAngle, 0, 180);
      middleAngle = constrain(middleAngle, 0, 180);
      ringAngle = constrain(ringAngle, 0, 180);
      pinkyAngle = constrain(pinkyAngle, 0, 180);
      thumbAngle = constrain(thumbAngle, 0, 180);

      // Gerakkan servo ke sudut yang telah ditentukan
      indexServo.write(indexAngle);
      middleServo.write(middleAngle);
      ringServo.write(ringAngle);
      pinkyServo.write(pinkyAngle);
      thumbServo.write(thumbAngle);

      // Cetak sudut ke Serial Monitor untuk debugging
      Serial.print("Index Angle: ");
      Serial.print(indexAngle);
      Serial.print(" Middle Angle: ");
      Serial.print(middleAngle);
      Serial.print(" Ring Angle: ");
      Serial.print(ringAngle);
      Serial.print(" Pinky Angle: ");
      Serial.print(pinkyAngle);
      Serial.print(" Thumb Angle: ");
      Serial.println(thumbAngle);
    }
  }
}
