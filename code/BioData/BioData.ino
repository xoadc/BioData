#include "Heart.h"
#include "Respiration.h"
#include "SkinConductance.h"

Heart heart(A6);
Respiration resp(A3);
SkinConductance skin(A0);

//variable for attenuating data flow to serial port prevents crashes
const long printInterval = 20;       // millis

boolean heartDoOnce = true;    // for only performing actions once when heartbeat is detected
boolean respDoOnce = true;    // for only performing actions once when breath is detected

void setup() {
  Serial.begin(19200);  // works best in testing with 9600 or lower
  
  // Initialize sensor.
  heart.reset();
  resp.reset();
  skin.reset();
}

void loop() {

  // Update sensor.
  heart.update();
  resp.update();
  skin.update();

  unsigned long currentMillis = millis();    // update time
  
  if (currentMillis % printInterval == 0) {  //impose a delay to avoid taxing your serial port
    
    Serial.print("H:");
    Serial.print(heart.getNormalized());  

    Serial.print(" R:");
    Serial.print(resp.getNormalized()); 

    Serial.print(" S:");
    Serial.println((1024.0f / (float)skin.getRaw()) - 1.0f);
    
  } 

}

