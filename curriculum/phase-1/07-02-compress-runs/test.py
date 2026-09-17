import unittest

from solution import compress_runs


class TestCompressRuns(unittest.TestCase):
    def test_mixed_runs(self):
        self.assertEqual(compress_runs("aaabcc"), "a3bc2")

    def test_no_repeats_stays_the_same(self):
        self.assertEqual(compress_runs("abc"), "abc")

    def test_same_character_in_separate_runs(self):
        self.assertEqual(compress_runs("aabbaa"), "a2b2a2")

    def test_case_sensitive(self):
        self.assertEqual(compress_runs("aAA"), "aA2")

    def test_empty_string(self):
        self.assertEqual(compress_runs(""), "")

    def test_single_character(self):
        self.assertEqual(compress_runs("z"), "z")

    def test_last_run_is_included(self):
        self.assertEqual(compress_runs("abcccc"), "abc4")

    def test_run_length_of_two_or_more_digits(self):
        self.assertEqual(compress_runs("xxxxxxxxxxxxy"), "x12y")

    def test_spaces_and_punctuation_are_characters_too(self):
        self.assertEqual(compress_runs("hi!!  ok"), "hi!2 2ok")


if __name__ == "__main__":
    unittest.main(verbosity=2)
