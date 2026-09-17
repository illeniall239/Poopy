import unittest

from solution import binary_search

ODDS = [1, 3, 5, 7, 9, 11]


class TestBinarySearch(unittest.TestCase):
    def test_finds_a_value_in_the_middle(self):
        self.assertEqual(binary_search(ODDS, 7), 3)
        self.assertEqual(binary_search(ODDS, 5), 2)

    def test_finds_the_first_and_last_values(self):
        self.assertEqual(binary_search(ODDS, 1), 0)
        self.assertEqual(binary_search(ODDS, 11), 5)

    def test_missing_value_between_two_elements(self):
        self.assertEqual(binary_search(ODDS, 4), -1)

    def test_missing_value_below_and_above_the_range(self):
        self.assertEqual(binary_search(ODDS, 0), -1)
        self.assertEqual(binary_search(ODDS, 12), -1)

    def test_empty_list(self):
        self.assertEqual(binary_search([], 5), -1)

    def test_one_and_two_elements(self):
        self.assertEqual(binary_search([5], 5), 0)
        self.assertEqual(binary_search([5], 6), -1)
        self.assertEqual(binary_search([2, 4], 4), 1)
        self.assertEqual(binary_search([2, 4], 3), -1)

    def test_negative_and_very_large_values(self):
        values = [-2000000000, -7, 0, 1999999999, 2000000000]
        self.assertEqual(binary_search(values, -2000000000), 0)
        self.assertEqual(binary_search(values, 2000000000), 4)
        self.assertEqual(binary_search(values, 1), -1)

    def test_20000_searches_in_1000000_values_in_log_time(self):
        n = 1000000
        evens = list(range(0, 2 * n, 2))
        wrong = 0
        for q in range(20000):
            i = (q * 7919) % n
            if binary_search(evens, 2 * i) != i:
                wrong += 1
            if binary_search(evens, 2 * i + 1) != -1:
                wrong += 1
        self.assertEqual(wrong, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
