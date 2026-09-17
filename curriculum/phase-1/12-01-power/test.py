import unittest

from solution import power


class TestPower(unittest.TestCase):
    def test_even_exponent(self):
        self.assertEqual(power(2, 10), 1024)

    def test_odd_exponent(self):
        self.assertEqual(power(3, 5), 243)
        self.assertEqual(power(3, 13), 1594323)

    def test_exponent_0_gives_1_even_for_base_0(self):
        self.assertEqual(power(5, 0), 1)
        self.assertEqual(power(0, 0), 1)

    def test_exponent_1_gives_the_base(self):
        self.assertEqual(power(7, 1), 7)

    def test_negative_base_keeps_the_right_sign(self):
        self.assertEqual(power(-2, 3), -8)
        self.assertEqual(power(-2, 4), 16)

    def test_decimal_base(self):
        self.assertEqual(power(0.5, 3), 0.125)

    def test_huge_exponent_finishes_without_overflowing_the_stack(self):
        self.assertEqual(power(1, 1000000000), 1)
        self.assertEqual(power(-1, 999999999), -1)
        self.assertEqual(power(2, 1023), 2 ** 1023)


if __name__ == "__main__":
    unittest.main(verbosity=2)
