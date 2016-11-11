/*
  50A Current Sensor(DC)(SKU:SEN0098) Sample Code
  This code shows you how to get raw datas from the sensor through Arduino and
  convert the raw datas to the value of the current according to the datasheet;

  Smoothing algorithm (http://www.arduino.cc/en/Tutorial/Smoothing) is used to
  make the outputting current value more reliable;

  Created 27 December 2011 @Barry Machine @www.dfrobot.com
*/

const int numReadings = 10;
float readings[numReadings];      // the readings from the analog input
int index = 0;                  // the index of the current reading
float total = 0;                  // the running total
float average = 0;                // the average

float currentValue = 0;
float energy = 0;


void setup()
{
  Serial.begin(115200);
  for (int thisReading = 0; thisReading < numReadings; thisReading++)
    readings[thisReading] = 0;
}


void loop()
{
  total = total - readings[index];
  readings[index] = analogRead(0); //Raw data reading
  //Data processing:510-raw data from analogRead when the input is 0;
  // 5-5v; the first 0.04-0.04V/A(sensitivity); the second 0.04-offset val;
  readings[index] = (readings[index] - 512) * 5 / 1024 / 0.04 - 0.04;

  total = total + readings[index];
  index = index + 1;
  if (index >= numReadings)
    index = 0;
  average = total / numReadings; //Smoothing algorithm (http://www.arduino.cc/en/Tutorial/Smoothing)
  currentValue = average;
  if (currentValue < 0.2)
    currentValue = 0.0;
  Serial.print("a\t");
  Serial.println(currentValue);

  delay(100);

}
