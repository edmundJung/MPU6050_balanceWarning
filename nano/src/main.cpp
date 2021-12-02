#include <Arduino.h>
#include <Ultrasonic.h>

#define pressure_sensor_first A0
#define pressure_sensor_second A1
#define Trigger 2
#define Echo 5

Ultrasonic ultrasonic(Trigger, Echo);
float pressure_1 = 0;
float pressure_2 = 0;
float distance = 0;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  ultrasonic.setTimeout(40000UL);
}

void loop()
{
  Serial.print(ultrasonic.read());
  Serial.print(";");
  Serial.print(analogRead(pressure_sensor_first));
  Serial.print(";");
  Serial.println(analogRead(pressure_sensor_second));
}