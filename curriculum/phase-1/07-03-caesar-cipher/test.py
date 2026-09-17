import unittest

from solution import caesar_shift


class TestCaesarShift(unittest.TestCase):
    def test_shift_by_one(self):
        self.assertEqual(caesar_shift("abc", 1), "bcd")

    def test_wraps_past_z(self):
        self.assertEqual(caesar_shift("xyz", 3), "abc")

    def test_keeps_case_and_non_letters(self):
        self.assertEqual(caesar_shift("Hello, World!", 5), "Mjqqt, Btwqi!")

    def test_uppercase_wraps_within_uppercase(self):
        self.assertEqual(caesar_shift("XYZ", 2), "ZAB")

    def test_negative_shift_wraps_backwards(self):
        self.assertEqual(caesar_shift("bcd", -1), "abc")
        self.assertEqual(caesar_shift("aB", -1), "zA")

    def test_shifts_larger_than_26(self):
        self.assertEqual(caesar_shift("abc", 27), "bcd")
        self.assertEqual(caesar_shift("abc", 26), "abc")
        self.assertEqual(caesar_shift("a", -27), "z")
        self.assertEqual(caesar_shift("Hi", 1000000), caesar_shift("Hi", 1000000 % 26))

    def test_digits_and_spaces_unchanged_empty_string_stays_empty(self):
        self.assertEqual(caesar_shift("route 66", 1), "spvuf 66")
        self.assertEqual(caesar_shift("", 5), "")

    def test_shifting_back_undoes_the_shift(self):
        secret = caesar_shift("Meet at 9pm, Zoe!", 11)
        self.assertEqual(caesar_shift(secret, -11), "Meet at 9pm, Zoe!")


if __name__ == "__main__":
    unittest.main(verbosity=2)
