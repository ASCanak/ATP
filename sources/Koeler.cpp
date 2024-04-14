#ifndef KOELER_CPP_
#define KOELER_CPP_

#include <iostream>
#include "DHT11.cpp"

class Koeler {
    private: 
        static bool status; 
    public:
        static void start() {
            minUpdate = -1.0f;
            status = true;
        }

        static void stop() {
            minUpdate = -0.5f;
            status = false;
        }

        static bool getStatus() { return status; }
};

bool Koeler::status = false;

extern "C" {
    // Define C-style functions to mimic the behavior of the Koeler class
    void Koeler_start()     { Koeler::start();            }
    void Koeler_stop()      { Koeler::stop();             }
    bool Koeler_getStatus() { return Koeler::getStatus(); }
}

#endif