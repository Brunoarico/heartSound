#define USE_ARDUINO_INTERRUPTS true
#include <PulseSensorPlayground.h>


const int PULSE_SENSOR_COUNT = 6;

const int PULSE_INPUT[6] = {A0, A1, A2, A3, A4, A5};

const int THRESHOLD = 550;   // Adjust this number to avoid noise when idle

PulseSensorPlayground pulseSensor(PULSE_SENSOR_COUNT);

void setup() {

  Serial.begin(115200);
  
  for(int i  = 0; i < PULSE_SENSOR_COUNT; i++)
    pulseSensor.analogInput(PULSE_INPUT[i], i);
    
  pulseSensor.setThreshold(THRESHOLD);
    
  if (!pulseSensor.begin()) {
    for (;;) {
      // Flash the led to show things didn't work.
      digitalWrite(13, LOW);
      delay(50);
      digitalWrite(13, HIGH);
      delay(50);
    }
  }
}

void loop() {
  delay(20);
  String v = "";
  for (int i = 0; i < PULSE_SENSOR_COUNT; ++i) {
    if (pulseSensor.sawStartOfBeat(i)) v+="1";
    else v+="0";
  }
  v+="\n";
  Serial.print(v);
}
