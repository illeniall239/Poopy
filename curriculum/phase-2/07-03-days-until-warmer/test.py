import unittest

from solution import days_until_warmer


class TestDaysUntilWarmer(unittest.TestCase):
    def test_mixed_week(self):
        self.assertEqual(days_until_warmer([73, 74, 75, 71, 69, 72, 76, 73]), [1, 1, 4, 2, 1, 1, 0, 0])

    def test_rising_temperatures(self):
        self.assertEqual(days_until_warmer([30, 40, 50, 60]), [1, 1, 1, 0])

    def test_falling_temperatures_never_get_warmer(self):
        self.assertEqual(days_until_warmer([60, 50, 40]), [0, 0, 0])

    def test_equal_temperature_is_not_warmer(self):
        self.assertEqual(days_until_warmer([5, 5, 6]), [2, 1, 0])
        self.assertEqual(days_until_warmer([7, 7, 7]), [0, 0, 0])

    def test_empty_and_single_day(self):
        self.assertEqual(days_until_warmer([]), [])
        self.assertEqual(days_until_warmer([-3]), [0])

    def test_negative_temperatures(self):
        self.assertEqual(days_until_warmer([-10, -20, -5, -30, 0]), [2, 1, 2, 1, 0])

    def test_does_not_change_the_input(self):
        temps = [3, 1, 2]
        days_until_warmer(temps)
        self.assertEqual(temps, [3, 1, 2])

    def test_200000_days_in_linear_time(self):
        n = 200000
        temps = [n - i for i in range(n - 1)] + [n + 1]
        self.assertEqual(days_until_warmer(temps), [n - 1 - i for i in range(n - 1)] + [0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
