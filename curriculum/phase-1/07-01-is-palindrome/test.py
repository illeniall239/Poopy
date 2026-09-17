import unittest

from solution import is_palindrome


class TestIsPalindrome(unittest.TestCase):
    def test_simple_lowercase_palindrome(self):
        self.assertEqual(is_palindrome("racecar"), True)

    def test_sentence_with_spaces_and_punctuation(self):
        self.assertEqual(is_palindrome("A man, a plan, a canal: Panama!"), True)

    def test_not_a_palindrome(self):
        self.assertEqual(is_palindrome("hello"), False)

    def test_case_is_ignored(self):
        self.assertEqual(is_palindrome("Aa"), True)
        self.assertEqual(is_palindrome("No 'x' in Nixon"), True)

    def test_digits_are_ignored(self):
        self.assertEqual(is_palindrome("Ab1a"), True)
        self.assertEqual(is_palindrome("a12b"), False)

    def test_empty_string_and_no_letters_are_palindromes(self):
        self.assertEqual(is_palindrome(""), True)
        self.assertEqual(is_palindrome("?! 42"), True)

    def test_almost_a_palindrome_fails_in_the_middle(self):
        self.assertEqual(is_palindrome("abcxba"), False)

    def test_even_and_odd_lengths(self):
        self.assertEqual(is_palindrome("abba"), True)
        self.assertEqual(is_palindrome("abcba"), True)
        self.assertEqual(is_palindrome("ab"), False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
