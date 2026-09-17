import unittest

from solution import group_anagrams


class TestGroupAnagrams(unittest.TestCase):
    def test_groups_anagrams_in_order_of_first_appearance(self):
        self.assertEqual(
            group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]),
            [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]],
        )

    def test_different_lengths_are_never_anagrams(self):
        self.assertEqual(group_anagrams(["ab", "abc", "ba"]), [["ab", "ba"], ["abc"]])

    def test_empty_input(self):
        self.assertEqual(group_anagrams([]), [])

    def test_no_anagrams_gives_one_group_per_word(self):
        self.assertEqual(group_anagrams(["cat", "dog", "bird"]), [["cat"], ["dog"], ["bird"]])

    def test_same_letters_but_different_counts_are_not_anagrams(self):
        self.assertEqual(group_anagrams(["aab", "abb", "bab"]), [["aab"], ["abb", "bab"]])

    def test_duplicate_words_stay_in_the_same_group(self):
        self.assertEqual(group_anagrams(["stop", "pots", "stop"]), [["stop", "pots", "stop"]])

    def test_does_not_modify_the_input(self):
        words = ["tops", "spot", "a"]
        group_anagrams(words)
        self.assertEqual(words, ["tops", "spot", "a"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
