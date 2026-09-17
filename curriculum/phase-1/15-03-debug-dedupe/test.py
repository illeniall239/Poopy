import unittest

from solution import dedupe


class TestDedupe(unittest.TestCase):
    def test_removes_scattered_duplicates_keeping_first_appearances(self):
        self.assertEqual(dedupe([1, 2, 1, 3, 2]), [1, 2, 3])

    def test_removes_runs_of_the_same_number(self):
        self.assertEqual(dedupe([5, 5, 5, 5]), [5])
        self.assertEqual(dedupe([1, 1, 2, 2, 2, 3]), [1, 2, 3])

    def test_empty_list(self):
        self.assertEqual(dedupe([]), [])

    def test_does_not_change_the_input(self):
        input = [4, 4, 7]
        self.assertEqual(dedupe(input), [4, 7])
        self.assertEqual(input, [4, 4, 7])

    def test_returns_a_new_list_even_without_duplicates(self):
        input = [3, 1, 2]
        result = dedupe(input)
        self.assertEqual(result, [3, 1, 2])
        self.assertIsNot(result, input)

    def test_keeps_the_position_of_each_first_appearance(self):
        self.assertEqual(dedupe([2, 9, 2, 9, 0, 2]), [2, 9, 0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
