import unittest

from solution import longest_unique_substring


class TestLongestUniqueSubstring(unittest.TestCase):
    def test_repeating_pattern(self):
        self.assertEqual(longest_unique_substring("abcabcbb"), 3)

    def test_one_repeated_character(self):
        self.assertEqual(longest_unique_substring("bbbbb"), 1)

    def test_substring_must_be_contiguous(self):
        self.assertEqual(longest_unique_substring("pwwkew"), 3)
        self.assertEqual(longest_unique_substring("dvdf"), 3)

    def test_left_edge_never_moves_backwards(self):
        self.assertEqual(longest_unique_substring("abba"), 2)
        self.assertEqual(longest_unique_substring("tmmzuxt"), 5)

    def test_all_characters_distinct(self):
        self.assertEqual(longest_unique_substring("abcdef"), 6)
        self.assertEqual(longest_unique_substring("x"), 1)

    def test_empty_string_gives_0(self):
        self.assertEqual(longest_unique_substring(""), 0)

    def test_spaces_digits_and_non_ascii_characters_count_as_characters(self):
        self.assertEqual(longest_unique_substring("a b a"), 3)
        self.assertEqual(longest_unique_substring("1231"), 3)
        self.assertEqual(longest_unique_substring("ñañb"), 3)

    def test_16000_characters_over_a_large_alphabet_in_o_n(self):
        m = 8000
        distinct = "".join(chr(0x100 + i) for i in range(m))
        self.assertEqual(longest_unique_substring(distinct + distinct), m)


if __name__ == "__main__":
    unittest.main(verbosity=2)
