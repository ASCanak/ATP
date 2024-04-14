from decorators import measure_time
from main import Thermostaat
import unittest

class unitTest(unittest.TestCase):
    @measure_time
    def test_koeler_aan(self):
        result = Thermostaat.logic(actualTemp = 25.0, desiredTemp = 20.0, coolerOn = False)
        self.assertEqual(result, "start", "Het 'start' signaal hoort gegeven te zijn!")

        result = Thermostaat.logic(actualTemp = 30.0, desiredTemp = 25.0, coolerOn = False)
        self.assertEqual(result, "start", "Het 'start' signaal hoort gegeven te zijn!")
    
    @measure_time
    def test_koeler_uit(self):
        result = Thermostaat.logic(actualTemp = 20.0, desiredTemp = 25.0, coolerOn = True)
        self.assertEqual(result, "stop", "Het 'stop' signaal hoort gegeven te zijn!")

        result = Thermostaat.logic(actualTemp = 25.0, desiredTemp = 30.0, coolerOn = True)
        self.assertEqual(result, "stop", "Het 'stop' signaal hoort gegeven te zijn!")

    @measure_time
    def test_koeler_aan_blijven(self):
        result = Thermostaat.logic(actualTemp = 25.0, desiredTemp = 20.0, coolerOn = True)
        self.assertEqual(result, "none", "Het 'none' signaal hoort gegeven te zijn!")

        result = Thermostaat.logic(actualTemp = 30.0, desiredTemp = 25.0, coolerOn = True)
        self.assertEqual(result, "none", "Het 'none' signaal hoort gegeven te zijn!")

    @measure_time
    def test_koeler_uit_blijven(self):
        result = Thermostaat.logic(actualTemp = 20.0, desiredTemp = 25.0, coolerOn = False)
        self.assertEqual(result, "none", "Het 'none' signaal hoort gegeven te zijn!")

        result = Thermostaat.logic(actualTemp = 25.0, desiredTemp = 30.0, coolerOn = False)
        self.assertEqual(result, "none", "Het 'none' signaal hoort gegeven te zijn!")


if __name__ == "__main__":
    unittest.main()