import unittest

from solution import fewest_removals


class TestFewestRemovals(unittest.TestCase):
    def test_one_interval_overlaps_two_others(self):
        self.assertEqual(fewest_removals([[1, 2], [2, 3], [3, 4], [1, 3]]), 1)

    def test_identical_intervals_overlap_each_other(self):
        self.assertEqual(fewest_removals([[1, 2], [1, 2], [1, 2]]), 2)

    def test_touching_intervals_do_not_overlap(self):
        self.assertEqual(fewest_removals([[1, 2], [2, 3]]), 0)

    def test_one_long_interval_covering_several_short_ones(self):
        self.assertEqual(fewest_removals([[1, 10], [2, 3], [4, 5], [6, 7]]), 1)

    def test_empty_list_and_single_interval(self):
        self.assertEqual(fewest_removals([]), 0)
        self.assertEqual(fewest_removals([[5, 9]]), 0)

    def test_negative_coordinates(self):
        self.assertEqual(fewest_removals([[-5, -1], [-3, 2], [0, 4], [3, 6]]), 2)

    def test_nested_intervals(self):
        self.assertEqual(fewest_removals([[1, 100], [2, 50], [3, 25], [4, 10]]), 3)

    def test_unsorted_input_is_not_changed(self):
        intervals = [[3, 4], [1, 2], [2, 3]]
        self.assertEqual(fewest_removals(intervals), 0)
        self.assertEqual(intervals, [[3, 4], [1, 2], [2, 3]])

    def test_100000_intervals_in_n_log_n(self):
        k_count = 50000
        intervals = []
        for i in range(2 * k_count):
            idx = (i * 7919) % (2 * k_count)
            k = idx // 2
            intervals.append([2 * k, 2 * k + 2] if idx % 2 == 0 else [2 * k + 1, 2 * k + 3])
        self.assertEqual(fewest_removals(intervals), k_count)


if __name__ == "__main__":
    unittest.main(verbosity=2)
