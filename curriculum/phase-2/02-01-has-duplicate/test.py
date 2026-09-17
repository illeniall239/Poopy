import unittest

from solution import has_duplicate


class TestHasDuplicate(unittest.TestCase):
    def test_finds_a_repeated_value(self):
        self.assertTrue(has_duplicate([1, 2, 3, 1]))

    def test_all_distinct_values(self):
        self.assertFalse(has_duplicate([1, 2, 3]))

    def test_empty_list_has_no_duplicates(self):
        self.assertFalse(has_duplicate([]))

    def test_a_single_value_is_not_a_duplicate_of_itself(self):
        self.assertFalse(has_duplicate([7]))

    def test_negative_values_and_their_opposites_are_different(self):
        self.assertFalse(has_duplicate([-1, 1, -2, 2, 0]))
        self.assertTrue(has_duplicate([-5, 3, -5]))

    def test_duplicates_as_the_last_two_values(self):
        self.assertTrue(has_duplicate([4, 8, 15, 16, 23, 42, 42]))

    def test_does_not_change_the_input(self):
        values = [3, 1, 2, 3]
        has_duplicate(values)
        self.assertEqual(values, [3, 1, 2, 3])

    def test_50000_distinct_values_in_o_n(self):
        n = 50000
        values = [(i * 7919) % n for i in range(n)]
        self.assertFalse(has_duplicate(values))


if __name__ == "__main__":
    unittest.main(verbosity=2)
