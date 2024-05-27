import unittest
from temp_code_2 import process_user_data

class TestProcessUserData(unittest.TestCase):

    def test_complete_data(self):
        # Testujeme, že funkcia správne spracuje kompletné dáta
        self.assertEqual(process_user_data({"name": "Alice", "age": 25, "active": True}),
                         {"name": "Alice", "age": 25, "status": "Active"})

    def test_missing_values(self):
        # Testujeme, že funkcia správne zvláda chýbajúce hodnoty a nastaví predvolené hodnoty
        self.assertEqual(process_user_data({"name": "", "age": None, "active": None}),
                         {"name": "Unknown", "age": 18, "status": "Active"})

    def test_partial_data(self):
        # Testujeme, že funkcia správne zvláda čiastočné dáta
        self.assertEqual(process_user_data({"name": "Bob"}),
                         {"name": "Bob", "age": 18, "status": "Active"})

    def test_inactive_status(self):
        # Testujeme, že funkcia správne nastaví status na "Inactive" ak active je False
        self.assertEqual(process_user_data({"name": "Charlie", "age": 30, "active": False}),
                         {"name": "Charlie", "age": 30, "status": "Inactive"})

if __name__ == '__main__':
    unittest.main()
