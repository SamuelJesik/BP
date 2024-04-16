import unittest
from temp_code_2 import calculate_squares  # Importujeme vašu funkciu pre testovanie



class TestCalculateSquares(unittest.TestCase):

    def test_calculate_squares(self):
        # Testujeme, že funkcia vracia správne výsledky pre známe vstupy
        self.assertEqual(calculate_squares(10), [0, 1, 4, 9, 16, 25, 36, 49, 64, 81])

    def test_calculate_squares_empty(self):
        # Testujeme, že funkcia vracia prázdny zoznam, keď je vstup nula
        self.assertEqual(calculate_squares(0), [])



# Tento kód umožňuje spustiť testy, keď súbor spustíte priamo
if __name__ == '__main__':
    unittest.main()