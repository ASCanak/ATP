#ifndef ROLLUIK_CPP_
#define ROLLUIK_CPP_

#include <iostream>

class Rolluik {
    private: 
        static bool status; 
    public:
        static void close()     { status = true;  }
        static void open()      { status = false; }
        static bool getStatus() { return status;  }
};

bool Rolluik::status = false;

extern "C" {
    // Define C-style functions to mimic the behavior of the Rolluik class
    void Rolluik_close()     { Rolluik::close();            }
    void Rolluik_open()      { Rolluik::open();             }
    bool Rolluik_getStatus() { return Rolluik::getStatus(); }
}

#endif