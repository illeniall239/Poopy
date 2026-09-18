import unittest

import numpy as np

from solution import pearson, rank, spearman


def numpy_rank(v):
    v = np.asarray(v, float)
    order = np.argsort(v, kind="stable")
    ranks = np.empty(len(v))
    ranks[order] = np.arange(1, len(v) + 1)
    for val in np.unique(v):
        mask = v == val
        ranks[mask] = ranks[mask].mean()
    return ranks


class TestCorrelation(unittest.TestCase):
    def test_pearson_perfect(self):
        self.assertAlmostEqual(pearson([1, 2, 3], [2, 4, 6]), 1.0)
        self.assertAlmostEqual(pearson([1, 2, 3], [3, 2, 1]), -1.0)

    def test_pearson_partial(self):
        self.assertAlmostEqual(pearson([1, 2, 3, 4], [1, 3, 2, 4]), 0.8)

    def test_pearson_errors(self):
        with self.assertRaises(ValueError):
            pearson([1, 2], [1])
        with self.assertRaises(ValueError):
            pearson([1], [2])
        with self.assertRaises(ValueError):
            pearson([1, 1, 1], [1, 2, 3])

    def test_rank_with_ties(self):
        self.assertEqual(rank([10, 20, 20, 30]), [1.0, 2.5, 2.5, 4.0])
        self.assertEqual(rank([5, 5, 5]), [2.0, 2.0, 2.0])
        self.assertEqual(rank([3, 1, 2]), [3.0, 1.0, 2.0])
        self.assertEqual(rank([1, 1, 2, 2, 2, 3]), [1.5, 1.5, 4.0, 4.0, 4.0, 6.0])

    def test_spearman_monotone(self):
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 9, 16, 25]
        self.assertAlmostEqual(spearman(x, y), 1.0)
        self.assertLess(pearson(x, y), 1.0)
        self.assertGreater(pearson(x, y), 0.97)

    def test_spearman_robust_to_outlier(self):
        x = list(range(1, 21))
        y = list(range(1, 21))
        y[-1] = 10_000
        self.assertAlmostEqual(spearman(x, y), 1.0)
        self.assertLess(pearson(x, y), 0.7)

    def test_matches_numpy_random(self):
        rng = np.random.default_rng(0)
        for _ in range(5):
            x = rng.normal(size=300)
            y = 0.6 * x + rng.normal(size=300)
            self.assertAlmostEqual(pearson(x.tolist(), y.tolist()), float(np.corrcoef(x, y)[0, 1]), places=9)
            expected_s = float(np.corrcoef(numpy_rank(x), numpy_rank(y))[0, 1])
            self.assertAlmostEqual(spearman(x.tolist(), y.tolist()), expected_s, places=9)

    def test_rank_matches_numpy_with_many_ties(self):
        rng = np.random.default_rng(1)
        v = rng.integers(0, 10, size=5000).tolist()
        np.testing.assert_allclose(rank(v), numpy_rank(v))
        y = rng.integers(0, 10, size=5000).tolist()
        expected = float(np.corrcoef(numpy_rank(v), numpy_rank(y))[0, 1])
        self.assertAlmostEqual(spearman(v, y), expected, places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
