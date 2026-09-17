import unittest

from solution import first_unique_index


class TestFirstUniqueIndex(unittest.TestCase):
    def test_first_character_is_unique(self):
        self.assertEqual(first_unique_index("leetcode"), 0)

    def test_unique_character_in_the_middle(self):
        self.assertEqual(first_unique_index("loveleetcode"), 2)

    def test_no_unique_character(self):
        self.assertEqual(first_unique_index("aabb"), -1)

    def test_empty_string(self):
        self.assertEqual(first_unique_index(""), -1)

    def test_case_sensitive(self):
        self.assertEqual(first_unique_index("aA"), 0)
        self.assertEqual(first_unique_index("aAa"), 1)

    def test_a_character_that_repeats_later_is_not_unique(self):
        self.assertEqual(first_unique_index("abcabd"), 2)

    def test_unique_character_at_the_end(self):
        self.assertEqual(first_unique_index("xyxyz"), 4)

    def test_spaces_count_as_characters(self):
        self.assertEqual(first_unique_index("aa bb"), 2)

    def test_long_string_is_handled_quickly(self):
        text = "ab" * 50000
        self.assertEqual(first_unique_index(text + "c"), 100000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
