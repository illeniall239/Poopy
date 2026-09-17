import unittest

from solution import permutations


class TestPermutations(unittest.TestCase):
    def test_two_characters(self):
        self.assertEqual(permutations("ab"), ["ab", "ba"])

    def test_three_characters_sorted(self):
        self.assertEqual(permutations("abc"), ["abc", "acb", "bac", "bca", "cab", "cba"])

    def test_input_order_does_not_change_the_sorted_result(self):
        self.assertEqual(permutations("cba"), ["abc", "acb", "bac", "bca", "cab", "cba"])

    def test_repeated_characters_give_distinct_results_only(self):
        self.assertEqual(permutations("aab"), ["aab", "aba", "baa"])
        self.assertEqual(permutations("aaa"), ["aaa"])

    def test_single_character(self):
        self.assertEqual(permutations("a"), ["a"])

    def test_empty_string_has_one_ordering(self):
        self.assertEqual(permutations(""), [""])

    def test_eight_distinct_characters_give_40320_distinct_results(self):
        result = permutations("abcdefgh")
        self.assertEqual(len(result), 40320)
        self.assertEqual(len(set(result)), 40320)
        self.assertEqual(result[0], "abcdefgh")
        self.assertEqual(result[40319], "hgfedcba")


if __name__ == "__main__":
    unittest.main(verbosity=2)
