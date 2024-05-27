import unittest
from temp_code_8 import StatisticsCalculator

class TestStatisticsCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = StatisticsCalculator([10, 20, 30, 40, 50])

    def test_analyze_data(self):
        results = self.calculator.analyze_data()
        self.assertEqual(results["minimum"], 10)
        self.assertEqual(results["maximum"], 50)
        self.assertAlmostEqual(results["mean"], 30.0)
        self.assertAlmostEqual(results["variance"], 250.0)
        self.assertEqual(results["count"], 5)

if __name__ == '__main__':
    unittest.main()
