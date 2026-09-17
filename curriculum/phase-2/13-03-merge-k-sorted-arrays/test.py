import unittest

from solution import merge_k_sorted


class TestMergeKSorted(unittest.TestCase):
    def test_three_interleaving_arrays(self):
        self.assertEqual(merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]]), [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_empty_inner_arrays_and_duplicates(self):
        self.assertEqual(merge_k_sorted([[], [1, 1, 3], [], [1, 2]]), [1, 1, 1, 2, 3])

    def test_no_arrays_at_all(self):
        self.assertEqual(merge_k_sorted([]), [])

    def test_a_single_array(self):
        self.assertEqual(merge_k_sorted([[-3, 0, 2]]), [-3, 0, 2])

    def test_negatives_and_different_lengths(self):
        self.assertEqual(
            merge_k_sorted([[-10, -5, 0, 5], [-7], [1, 2, 3, 4, 100]]),
            [-10, -7, -5, 0, 1, 2, 3, 4, 5, 100],
        )

    def test_does_not_change_the_input_arrays(self):
        data = [[1, 3], [2, 4]]
        merge_k_sorted(data)
        self.assertEqual(data, [[1, 3], [2, 4]])

    def test_5000_arrays_of_10_values_n_log_k(self):
        k, m = 5000, 10
        arrays = [[i * k + j for i in range(m)] for j in range(k)]
        self.assertEqual(merge_k_sorted(arrays), list(range(k * m)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
