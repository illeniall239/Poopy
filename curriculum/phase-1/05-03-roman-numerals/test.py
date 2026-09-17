import unittest

from solution import to_roman


class TestToRoman(unittest.TestCase):
    def test_ones_place_from_1_to_9(self):
        self.assertEqual(to_roman(1), "I")
        self.assertEqual(to_roman(3), "III")
        self.assertEqual(to_roman(4), "IV")
        self.assertEqual(to_roman(5), "V")
        self.assertEqual(to_roman(8), "VIII")
        self.assertEqual(to_roman(9), "IX")

    def test_tens_and_ones_together(self):
        self.assertEqual(to_roman(14), "XIV")
        self.assertEqual(to_roman(40), "XL")
        self.assertEqual(to_roman(90), "XC")

    def test_zero_digits_in_the_middle_write_nothing(self):
        self.assertEqual(to_roman(101), "CI")
        self.assertEqual(to_roman(2006), "MMVI")

    def test_hundreds_use_c_d_and_m(self):
        self.assertEqual(to_roman(400), "CD")
        self.assertEqual(to_roman(900), "CM")
        self.assertEqual(to_roman(500), "D")

    def test_every_place_at_once(self):
        self.assertEqual(to_roman(1994), "MCMXCIV")
        self.assertEqual(to_roman(3888), "MMMDCCCLXXXVIII")

    def test_largest_allowed_number(self):
        self.assertEqual(to_roman(3999), "MMMCMXCIX")

    def test_out_of_range_gives_an_empty_string(self):
        self.assertEqual(to_roman(0), "")
        self.assertEqual(to_roman(-5), "")
        self.assertEqual(to_roman(4000), "")

    def test_non_whole_numbers_give_an_empty_string(self):
        self.assertEqual(to_roman(2.5), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
