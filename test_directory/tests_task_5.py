import unittest
from temp_code_5 import price_assignment, ELECTRONICS, CLOTHING, FOOD, BOOKS, UNKNOWN

class TestPriceAssignment(unittest.TestCase):

    def test_electronics(self):
        self.assertEqual(price_assignment(ELECTRONICS), "Price set to $999")

    def test_clothing(self):
        self.assertEqual(price_assignment(CLOTHING), "Price set to $49")

    def test_food(self):
        self.assertEqual(price_assignment(FOOD), "Price set to $5")

    def test_books(self):
        self.assertEqual(price_assignment(BOOKS), "Price set to $15")

    def test_unknown(self):
        self.assertEqual(price_assignment("toys"), "Product type unknown")

if __name__ == '__main__':
    unittest.main()
