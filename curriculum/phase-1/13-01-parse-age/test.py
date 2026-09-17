import unittest

from solution import RangeError, parse_age


class TestParseAge(unittest.TestCase):
    def assert_raises_message(self, exc_type, message, input):
        with self.assertRaises(exc_type) as cm:
            parse_age(input)
        self.assertEqual(str(cm.exception), message)
        self.assertIs(type(cm.exception), exc_type)

    def test_parses_a_plain_age(self):
        self.assertEqual(parse_age("42"), 42)

    def test_ignores_surrounding_spaces_and_leading_zeros(self):
        self.assertEqual(parse_age("  7 "), 7)
        self.assertEqual(parse_age("007"), 7)

    def test_accepts_the_boundaries_0_and_150(self):
        self.assertEqual(parse_age("0"), 0)
        self.assertEqual(parse_age("150"), 150)

    def test_empty_or_blank_input_is_reported_as_empty_not_as_0(self):
        self.assert_raises_message(ValueError, "Age is empty", "")
        self.assert_raises_message(ValueError, "Age is empty", "   ")

    def test_non_digits_are_rejected_with_the_original_input_in_the_message(self):
        self.assert_raises_message(ValueError, 'Age must be a whole number, got "12.5"', "12.5")
        self.assert_raises_message(ValueError, 'Age must be a whole number, got "abc"', "abc")
        self.assert_raises_message(ValueError, 'Age must be a whole number, got " -5"', " -5")

    def test_inputs_that_int_or_float_would_accept_are_still_rejected(self):
        self.assert_raises_message(ValueError, 'Age must be a whole number, got "1e2"', "1e2")
        self.assert_raises_message(ValueError, 'Age must be a whole number, got "12abc"', "12abc")
        self.assert_raises_message(ValueError, 'Age must be a whole number, got "4 2"', "4 2")
        self.assert_raises_message(ValueError, 'Age must be a whole number, got "1_5"', "1_5")

    def test_too_old_is_a_range_error(self):
        self.assert_raises_message(RangeError, "Age must be between 0 and 150, got 151", "151")
        self.assert_raises_message(RangeError, "Age must be between 0 and 150, got 200", " 0200")


if __name__ == "__main__":
    unittest.main(verbosity=2)
