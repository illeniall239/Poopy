import unittest

from solution import is_leap_year


class TestIsLeapYear(unittest.TestCase):
    def test_divisible_by_4_is_a_leap_year(self):
        self.assertEqual(is_leap_year(2024), True)

    def test_not_divisible_by_4_is_not_a_leap_year(self):
        self.assertEqual(is_leap_year(2023), False)

    def test_divisible_by_100_but_not_400_is_not_a_leap_year(self):
        self.assertEqual(is_leap_year(1900), False)
        self.assertEqual(is_leap_year(2100), False)

    def test_divisible_by_400_is_a_leap_year(self):
        self.assertEqual(is_leap_year(2000), True)
        self.assertEqual(is_leap_year(2400), True)

    def test_even_but_not_divisible_by_4(self):
        self.assertEqual(is_leap_year(2022), False)

    def test_small_years_follow_the_same_rules(self):
        self.assertEqual(is_leap_year(4), True)
        self.assertEqual(is_leap_year(1), False)

    def test_returns_a_real_boolean(self):
        self.assertIsInstance(is_leap_year(2023), bool)


if __name__ == "__main__":
    unittest.main(verbosity=2)
