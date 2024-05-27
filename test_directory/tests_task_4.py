import unittest
from temp_code_4 import sum_and_average_of_list

class TestSumAndAverage(unittest.TestCase):

    def test_sum_and_average_with_data(self):
        # Test, či funkcia správne vypočíta sumu a priemer pre neprázdny zoznam
        result = sum_and_average_of_list([1, 2, 3, 4, 5])
        self.assertEqual(result, (15, 3.0))  # očakávaný výsledok je súčet 15 a priemer 3.0

    def test_sum_and_average_empty_list(self):
        # Test, či funkcia správne zvláda prázdny zoznam
        result = sum_and_average_of_list([])
        self.assertEqual(result, (0, 0))  # keďže zoznam je prázdny, suma aj priemer by mali byť 0

    def test_sum_and_average_single_element(self):
        # Test, či funkcia správne vypočíta sumu a priemer pre zoznam s jedným prvkom
        result = sum_and_average_of_list([42])
        self.assertEqual(result, (42, 42.0))  # suma aj priemer by mali byť rovnaké ako hodnota jediného prvku

    def test_sum_and_average_negative_numbers(self):
        # Test, či funkcia správne vypočíta sumu a priemer pre zoznam s negatívnymi číslami
        result = sum_and_average_of_list([-1, -2, -3, -4, -5])
        self.assertEqual(result, (-15, -3.0))  # očakávané výsledky sú suma -15 a priemer -3.0

if __name__ == '__main__':
    unittest.main()
