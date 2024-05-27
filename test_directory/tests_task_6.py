import unittest
from temp_code_6 import processData

class TestProcessSensorData(unittest.TestCase):

    def test_high_temperature(self):
        self.assertEqual(processData({"data": {"type": "temperature", "value": 35}}), "Hot")

    def test_low_temperature(self):
        self.assertEqual(processData({"data": {"type": "temperature", "value": 5}}), "Cold")

    def test_normal_temperature(self):
        self.assertEqual(processData({"data": {"type": "temperature", "value": 20}}), "Normal")

    def test_high_humidity(self):
        self.assertEqual(processData({"data": {"type": "humidity", "value": 85}}), "High Humidity")

    def test_low_humidity(self):
        self.assertEqual(processData({"data": {"type": "humidity", "value": 15}}), "Low Humidity")

    def test_normal_conditions(self):
        self.assertEqual(processData({"data": {"type": "humidity", "value": 50}}), "Normal")

if __name__ == '__main__':
    unittest.main()
