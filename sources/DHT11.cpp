#ifndef DHT11_CPP_
#define DHT11_CPP_

#include <iostream>
// Reading range [0 °C, 50 °C]
#define MIN_Temp 0
#define MAX_Temp 50

float temperature = 23.0; 

static float minUpdate = -0.5f;
static float maxUpdate = 1.0f;

extern "C" {
    float updateTemperature(float min, float max){
        return min + static_cast<float>(std::rand()) / (static_cast<float>(RAND_MAX / max));
    }

    float readTemperature(){
        temperature += updateTemperature(minUpdate, maxUpdate);
                
        // Quick ternary check if temperature < MIN_Temp or temperature > MAX_Temp.
        temperature = (temperature > MAX_Temp) ? MAX_Temp : (temperature < MIN_Temp) ? MIN_Temp : temperature;
        return temperature;        
    } 
}

#endif