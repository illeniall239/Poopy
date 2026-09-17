import unittest

from solution import fewest_coins


class TestFewestCoins(unittest.TestCase):
    def test_three_coins_make_11(self):
        self.assertEqual(fewest_coins([1, 2, 5], 11), 3)

    def test_largest_first_would_not_be_fewest(self):
        self.assertEqual(fewest_coins([1, 3, 4], 6), 2)

    def test_impossible_amount_gives_minus_1(self):
        self.assertEqual(fewest_coins([2], 3), -1)

    def test_amount_0_needs_no_coins(self):
        self.assertEqual(fewest_coins([1], 0), 0)

    def test_unsorted_coins(self):
        self.assertEqual(fewest_coins([7, 3], 23), 5)

    def test_amount_700_from_3_7_and_11(self):
        self.assertEqual(fewest_coins([3, 7, 11], 700), 64)

    def test_odd_amount_699_from_even_coins_is_impossible(self):
        self.assertEqual(fewest_coins([4, 6], 699), -1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
