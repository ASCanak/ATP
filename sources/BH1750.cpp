#ifndef BH1750_CPP_
#define BH1750_CPP_

#include <iostream>
// Reading range [0 Lux, 65535 Lux]
#define MIN_LL 0
#define MAX_LL 65535

float lightLevel = 0.0f; 
const int luxLevels[24] = { 0, 0, 0, 10, 15, 20, 100, 500, 
                            2000, 5000, 8000, 15000, 24000, 15000, 8000, 5000, 
                            3000, 1500, 800, 200, 50, 10, 5, 2};
unsigned int timeIndex = 0;

extern "C" {
    float updateLightLevel(){
        timeIndex = (timeIndex < 23) ? timeIndex + 1 : 0;
        return luxLevels[timeIndex];
    }

    float readLightLevel(){ 
        lightLevel = updateLightLevel();

        // Quick ternary check if lightLevel < MIN_LightLevel or lightLevel > MAX_LightLevel.
        lightLevel = (lightLevel > MAX_LL) ? MAX_LL : (lightLevel < MIN_LL) ? MIN_LL : lightLevel;
        return lightLevel;        
    } 
}

#endif