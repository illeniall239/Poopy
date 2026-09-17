import unittest

from solution import longest_common_subsequence


def make_string(n: int, m: int, mul: int) -> str:
    return "".join("acgt"[(i * i * mul + 3 * i + mul) % m % 4] for i in range(n))


class TestLongestCommonSubsequence(unittest.TestCase):
    def test_subsequence_of_the_other_string(self):
        self.assertEqual(longest_common_subsequence("abcde", "ace"), 3)

    def test_identical_strings(self):
        self.assertEqual(longest_common_subsequence("abc", "abc"), 3)

    def test_no_shared_characters(self):
        self.assertEqual(longest_common_subsequence("abc", "def"), 0)

    def test_empty_string(self):
        self.assertEqual(longest_common_subsequence("", "abc"), 0)

    def test_interleaved_matches(self):
        self.assertEqual(longest_common_subsequence("AGGTAB", "GXTXAYB"), 4)

    def test_repeated_characters_and_case_matters(self):
        self.assertEqual(longest_common_subsequence("aaaa", "aa"), 2)
        self.assertEqual(longest_common_subsequence("Abc", "abc"), 2)

    def test_two_400_character_strings_in_n_times_m(self):
        self.assertEqual(longest_common_subsequence(make_string(400, 7, 1), make_string(400, 11, 3)), 259)


if __name__ == "__main__":
    unittest.main(verbosity=2)
