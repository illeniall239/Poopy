import unittest

from solution import make_change


class TestMakeChange(unittest.TestCase):
    def test_one_of_each_coin_for_41(self):
        self.assertEqual(make_change(41), {"quarters": 1, "dimes": 1, "nickels": 1, "pennies": 1})

    def test_skips_coins_that_are_not_needed(self):
        self.assertEqual(make_change(30), {"quarters": 1, "dimes": 0, "nickels": 1, "pennies": 0})

    def test_zero_cents_gives_no_coins(self):
        self.assertEqual(make_change(0), {"quarters": 0, "dimes": 0, "nickels": 0, "pennies": 0})

    def test_pennies_only_below_5(self):
        self.assertEqual(make_change(4), {"quarters": 0, "dimes": 0, "nickels": 0, "pennies": 4})

    def test_exact_multiple_of_25(self):
        self.assertEqual(make_change(100), {"quarters": 4, "dimes": 0, "nickels": 0, "pennies": 0})

    def test_two_dimes_no_nickel_for_99(self):
        self.assertEqual(make_change(99), {"quarters": 3, "dimes": 2, "nickels": 0, "pennies": 4})

    def test_large_amount(self):
        self.assertEqual(make_change(100000), {"quarters": 4000, "dimes": 0, "nickels": 0, "pennies": 0})


if __name__ == "__main__":
    unittest.main(verbosity=2)
