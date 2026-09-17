import unittest

from solution import word_frequency


class TestWordFrequency(unittest.TestCase):
    def test_counts_repeated_words_in_order_of_first_appearance(self):
        result = word_frequency("the cat and the hat")
        self.assertIsInstance(result, dict)
        self.assertEqual(list(result.items()), [("the", 2), ("cat", 1), ("and", 1), ("hat", 1)])

    def test_case_insensitive_with_lowercase_keys(self):
        self.assertEqual(list(word_frequency("The THE the").items()), [("the", 3)])

    def test_punctuation_separates_words(self):
        self.assertEqual(list(word_frequency("Hi, hi! HI?").items()), [("hi", 3)])

    def test_digits_and_apostrophes_separate_words(self):
        self.assertEqual(list(word_frequency("abc123abc it's").items()), [("abc", 2), ("it", 1), ("s", 1)])

    def test_empty_text_and_text_without_words(self):
        self.assertEqual(len(word_frequency("")), 0)
        self.assertEqual(len(word_frequency("... 42 !")), 0)

    def test_word_at_the_very_end_is_counted(self):
        self.assertEqual(list(word_frequency("  go go").items()), [("go", 2)])

    def test_words_that_clash_with_builtin_names(self):
        self.assertEqual(
            list(word_frequency("constructor toString constructor").items()),
            [("constructor", 2), ("tostring", 1)],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
