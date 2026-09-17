import unittest

from solution import digit_sum_until_single


class TestDigitSumUntilSingle(unittest.TestCase):
    def test_one_pass_is_enough(self):
        self.assertEqual(digit_sum_until_single(16), 7)

    def test_needs_several_passes(self):
        self.assertEqual(digit_sum_until_single(493193), 2)

    def test_10_is_two_digits_and_becomes_1(self):
        self.assertEqual(digit_sum_until_single(10), 1)

    def test_a_single_digit_is_returned_unchanged(self):
        self.assertEqual(digit_sum_until_single(0), 0)
        self.assertEqual(digit_sum_until_single(9), 9)

    def test_sum_that_lands_exactly_on_10(self):
        self.assertEqual(digit_sum_until_single(19), 1)

    def test_zeros_inside_the_number(self):
        self.assertEqual(digit_sum_until_single(1000000), 1)

    def test_largest_safe_integer(self):
        self.assertEqual(digit_sum_until_single(9007199254740991), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
