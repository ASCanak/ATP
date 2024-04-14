from decorators import measure_time
from main import Thermostaat
from ctypes import *
import unittest

cmodule = CDLL('./clibrary.so')

# Defining c-types of readTemperature(None) -> float {};
cmodule.readTemperature.restype = c_float

# Defining c-types of getStatus(None) -> bool {} from the Rolluik class;
cmodule.Rolluik_getStatus.restype = c_bool

class integrationTest(unittest.TestCase):
    @measure_time
    def test_thermostat_logic_with_dht11(self):
        result = Thermostaat.logic(actualTemp = cmodule.readTemperature(), desiredTemp = 20.0, coolerOn = False)
        self.assertIn(result, ["start", "stop", "none"], "Unexpected Behaviour!")

        result = Thermostaat.logic(actualTemp = cmodule.readTemperature(), desiredTemp = 20.0, coolerOn = False)
        self.assertIn(result, ["start", "stop", "none"], "Unexpected Behaviour!")

    @measure_time
    def test_koeler_start(self):
        cmodule.Koeler_start()

        result = cmodule.Koeler_getStatus()
        self.assertEqual(result, True, "Status should be True!")

    @measure_time
    def test_koeler_stop(self):
        cmodule.Koeler_stop()  

        result = cmodule.Koeler_getStatus()
        self.assertEqual(result, False, "Status should be False!")

if __name__ == "__main__":
    unittest.main()