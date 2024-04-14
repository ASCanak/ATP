from decorators import measure_time
from main import Thermostaat
from ctypes import *
import unittest

cmodule = CDLL('./clibrary.so')

# Defining c-types of readTemperature(None) -> float {};
cmodule.readTemperature.restype = c_float

# Defining c-types of getStatus(None) -> bool {} from the Rolluik class;
cmodule.Rolluik_getStatus.restype = c_bool

class systemTest(unittest.TestCase):
    @measure_time
    def test_thermostaat_behavior(self):
        # Simulate the behavior of the system over multiple updates
        self.thermostaat = Thermostaat(desiredTemp = 23.0)
        
        for _ in range(24):  # Simulate 24 hours (updates)
            self.thermostaat.update()

            # Check if the cooling unit status matches the expected behavior
            cooler_status = cmodule.Koeler_getStatus()
            if cooler_status: #The room is hotter than it should be.
                self.assertTrue(self.thermostaat.actualTemp > self.thermostaat.desiredTemp - 1.0, "Unexpected Behaviour")
            else:             #The room is as cool as it should be.
                self.assertTrue(self.thermostaat.actualTemp < self.thermostaat.desiredTemp + 1.0, "Unexpected Behaviour")

if __name__ == "__main__":
    unittest.main()