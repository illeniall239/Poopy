import unittest

from solution import sum_of_multiples


class TestSumOfMultiples(unittest.TestCase):
    def test_multiples_below_10(self):
        self.assertEqual(sum_of_multiples(10), 23)

    def test_15_is_counted_once_not_twice(self):
        self.assertEqual(sum_of_multiples(16), 60)

    def test_n_itself_is_not_included(self):
        self.assertEqual(sum_of_multiples(3), 0)
        self.assertEqual(sum_of_multiples(15), 45)

    def test_the_first_multiple_just_below_n_is_included(self):
        self.assertEqual(sum_of_multiples(4), 3)

    def test_zero_and_one_give_zero(self):
        self.assertEqual(sum_of_multiples(0), 0)
        self.assertEqual(sum_of_multiples(1), 0)

    def test_larger_n(self):
        self.assertEqual(sum_of_multiples(1000), 233168)


if __name__ == "__main__":
    unittest.main(verbosity=2)
