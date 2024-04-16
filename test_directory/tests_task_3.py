# task_3_tests.py

import unittest
from temp_code_3 import calculate_squares  # Importujeme vašu funkciu pre testovanie



class TestCalculateSquares(unittest.TestCase):

    def test_calculate_squares(self):
        # Testujeme, že funkcia vracia správne výsledky pre známe vstupy
        self.assertEqual(calculate_squares(10), [0, 1, 4, 9, 16, 25, 36, 49, 64, 81],msg="Test 1 Passed")

    def test_calculate_squares_empty(self):
        # Testujeme, že funkcia vracia prázdny zoznam, keď je vstup nula
        self.assertEqual(calculate_squares(0), [],msg =" Test 2 Passed")

    def test_calculate_squares_negative(self):
        # Testujeme, že funkcia vracia prázdny zoznam, keď je vstup záporný
        self.assertEqual(calculate_squares(-5), [],msg =" Test 3 Passed")

# Tento kód umožňuje spustiť testy, keď súbor spustíte priamo
if __name__ == '__main__':
    unittest.main()
