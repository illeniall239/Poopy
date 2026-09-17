import unittest

from solution import has_lowercase, has_uppercase, has_digit, has_symbol, password_strength


class TestPasswordStrength(unittest.TestCase):
    def test_has_lowercase_and_has_uppercase_check_the_right_case(self):
        self.assertEqual(has_lowercase("ABc"), True)
        self.assertEqual(has_lowercase("ABC1!"), False)
        self.assertEqual(has_uppercase("abC"), True)
        self.assertEqual(has_uppercase("abc1!"), False)

    def test_has_digit_finds_a_digit_anywhere_including_0_and_9(self):
        self.assertEqual(has_digit("abc1"), True)
        self.assertEqual(has_digit("0abc"), True)
        self.assertEqual(has_digit("ab9c"), True)
        self.assertEqual(has_digit("abc"), False)

    def test_has_symbol_counts_anything_that_is_not_a_letter_or_digit(self):
        self.assertEqual(has_symbol("abc!"), True)
        self.assertEqual(has_symbol("a b"), True)
        self.assertEqual(has_symbol("aB3"), False)

    def test_helpers_return_false_for_an_empty_string(self):
        self.assertEqual(has_lowercase(""), False)
        self.assertEqual(has_uppercase(""), False)
        self.assertEqual(has_digit(""), False)
        self.assertEqual(has_symbol(""), False)

    def test_empty_password_scores_0_and_is_weak(self):
        self.assertEqual(password_strength(""), {"score": 0, "label": "weak"})

    def test_length_8_earns_a_point_score_2_is_still_weak(self):
        self.assertEqual(password_strength("abcdefg"), {"score": 1, "label": "weak"})
        self.assertEqual(password_strength("abcdefgh"), {"score": 2, "label": "weak"})

    def test_score_3_and_4_are_medium(self):
        self.assertEqual(password_strength("abcdefgH"), {"score": 3, "label": "medium"})
        self.assertEqual(password_strength("ABCDEFGHIJK1"), {"score": 4, "label": "medium"})

    def test_score_5_is_strong(self):
        self.assertEqual(password_strength("Abcdefg1!"), {"score": 5, "label": "strong"})

    def test_length_12_earns_an_extra_point_for_a_score_of_6(self):
        self.assertEqual(password_strength("Abcdefghij1"), {"score": 4, "label": "medium"})
        self.assertEqual(password_strength("Abcdefghij1!"), {"score": 6, "label": "strong"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
