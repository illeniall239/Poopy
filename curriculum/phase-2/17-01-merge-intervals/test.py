import unittest

from solution import merge_intervals


class TestMergeIntervals(unittest.TestCase):
    def test_merges_overlapping_neighbours(self):
        self.assertEqual(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]), [[1, 6], [8, 10], [15, 18]])

    def test_touching_endpoints_merge(self):
        self.assertEqual(merge_intervals([[1, 4], [4, 5]]), [[1, 5]])
        self.assertEqual(merge_intervals([[1, 3], [4, 5]]), [[1, 3], [4, 5]])

    def test_unsorted_input(self):
        self.assertEqual(merge_intervals([[8, 10], [1, 3], [2, 6]]), [[1, 6], [8, 10]])
        self.assertEqual(merge_intervals([[5, 6], [1, 2]]), [[1, 2], [5, 6]])

    def test_nested_intervals_disappear_into_the_outer_one(self):
        self.assertEqual(merge_intervals([[1, 10], [2, 3], [4, 5]]), [[1, 10]])
        self.assertEqual(merge_intervals([[2, 3], [1, 10]]), [[1, 10]])

    def test_a_chain_of_overlaps_merges_into_one(self):
        self.assertEqual(merge_intervals([[1, 2], [2, 3], [3, 4], [4, 5]]), [[1, 5]])

    def test_negative_bounds_and_single_point_intervals(self):
        self.assertEqual(merge_intervals([[-5, -1], [-2, 0], [3, 4]]), [[-5, 0], [3, 4]])
        self.assertEqual(merge_intervals([[5, 5], [5, 5], [7, 7]]), [[5, 5], [7, 7]])

    def test_empty_input_and_a_single_interval(self):
        self.assertEqual(merge_intervals([]), [])
        self.assertEqual(merge_intervals([[1, 2]]), [[1, 2]])

    def test_does_not_change_the_input_or_return_its_pairs(self):
        first = [4, 6]
        intervals = [first, [1, 5], [9, 9]]
        result = merge_intervals(intervals)
        self.assertEqual(result, [[1, 6], [9, 9]])
        self.assertEqual(intervals, [[4, 6], [1, 5], [9, 9]])
        self.assertEqual(first, [4, 6])
        self.assertTrue(all(pair is not original for pair in result for original in intervals), "result must hold new pairs")

    def test_200000_shuffled_disjoint_intervals_in_o_n_log_n(self):
        n = 200000
        intervals = [[3 * k, 3 * k + 1] for k in ((i * 7919) % n for i in range(n))]
        result = merge_intervals(intervals)
        self.assertEqual(len(result), n)
        self.assertTrue(all(pair == [3 * i, 3 * i + 1] for i, pair in enumerate(result)), "result is not sorted and disjoint")


if __name__ == "__main__":
    unittest.main(verbosity=2)
