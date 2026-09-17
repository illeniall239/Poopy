import unittest

from solution import smallest_covering_window


class TestSmallestCoveringWindow(unittest.TestCase):
    def test_classic_example(self):
        self.assertEqual(smallest_covering_window("ADOBECODEBANC", "ABC"), "BANC")

    def test_characters_may_appear_in_any_order(self):
        self.assertEqual(smallest_covering_window("abzcxcba", "abc"), "cba")
        self.assertEqual(smallest_covering_window("bba", "ab"), "ba")

    def test_leftmost_of_equally_short_windows(self):
        self.assertEqual(smallest_covering_window("acbxbca", "abc"), "acb")

    def test_repeats_in_t_must_be_covered(self):
        self.assertEqual(smallest_covering_window("aa", "aa"), "aa")
        self.assertEqual(smallest_covering_window("a", "aa"), "")
        self.assertEqual(smallest_covering_window("abcaba", "aab"), "aba")

    def test_whole_string_is_the_only_window(self):
        self.assertEqual(smallest_covering_window("a", "a"), "a")
        self.assertEqual(smallest_covering_window("xyz", "zyx"), "xyz")

    def test_empty_t_or_empty_s_gives_an_empty_string(self):
        self.assertEqual(smallest_covering_window("abc", ""), "")
        self.assertEqual(smallest_covering_window("", "a"), "")
        self.assertEqual(smallest_covering_window("", ""), "")

    def test_no_window_at_all(self):
        self.assertEqual(smallest_covering_window("abc", "d"), "")
        self.assertEqual(smallest_covering_window("ABC", "abc"), "")

    def test_30000_characters_with_the_window_at_the_end_in_o_n(self):
        n = 30000
        s = "a" * (n - 1) + "b"
        self.assertEqual(smallest_covering_window(s, "ab"), "ab")


if __name__ == "__main__":
    unittest.main(verbosity=2)
