import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import histogram


class TestHistogramCounts(unittest.TestCase):
    def test_small(self):
        counts, edges = histogram([1, 2, 2, 3, 4], 3)
        self.assertEqual(counts, [1, 2, 2])
        assert_allclose(edges, [1.0, 2.0, 3.0, 4.0])

    def test_two_values_two_bins(self):
        counts, edges = histogram([0, 10], 2)
        self.assertEqual(counts, [1, 1])
        assert_allclose(edges, [0.0, 5.0, 10.0])

    def test_all_equal(self):
        counts, edges = histogram([5, 5, 5], 2)
        self.assertEqual(counts, [0, 3])
        assert_allclose(edges, [4.5, 5.0, 5.5])

    def test_max_lands_in_last_bin(self):
        counts, _ = histogram([0, 1, 2, 3], 4)
        self.assertEqual(counts, [1, 1, 1, 1])

    def test_errors(self):
        with self.assertRaises(ValueError):
            histogram([], 3)
        with self.assertRaises(ValueError):
            histogram([1.0, 2.0], 0)

    def test_counts_sum_to_n(self):
        rng = np.random.default_rng(0)
        vals = rng.normal(size=1000).tolist()
        counts, edges = histogram(vals, 17)
        self.assertEqual(sum(counts), 1000)
        self.assertEqual(len(edges), 18)

    def test_matches_numpy_random(self):
        rng = np.random.default_rng(1)
        for bins in [1, 5, 10, 33, 100]:
            vals = rng.uniform(-3, 7, size=5000)
            counts, edges = histogram(vals.tolist(), bins)
            exp_counts, exp_edges = np.histogram(vals, bins)
            self.assertEqual(counts, exp_counts.tolist())
            assert_allclose(edges, exp_edges, atol=1e-9)

    def test_matches_numpy_on_integers_and_repeats(self):
        vals = [0, 1, 1, 2, 3, 3, 3, 7, 7, 10]
        for bins in [2, 3, 7, 10]:
            counts, edges = histogram(vals, bins)
            exp_counts, exp_edges = np.histogram(vals, bins)
            self.assertEqual(counts, exp_counts.tolist())
            assert_allclose(edges, exp_edges, atol=1e-9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
