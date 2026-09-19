import unittest

import numpy as np

from solution import explained_variance_ratio


def cloud(seed, scales, n=300):
    rng = np.random.default_rng(seed)
    d = len(scales)
    q, _ = np.linalg.qr(rng.normal(size=(d, d)))
    return (rng.normal(size=(n, d)) * np.array(scales)) @ q.T


class TestExplainedVariance(unittest.TestCase):
    def test_points_on_a_line(self):
        X = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])
        np.testing.assert_allclose(explained_variance_ratio(X, 2), [1.0, 0.0], atol=1e-12)

    def test_axis_aligned_rectangle(self):
        X = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 1.0], [2.0, 1.0]])
        got = explained_variance_ratio(X, 2)
        self.assertEqual(got.shape, (2,))
        np.testing.assert_allclose(got, [0.8, 0.2], atol=1e-12)
        np.testing.assert_allclose(explained_variance_ratio(X, 1), [0.8], atol=1e-12)

    def test_sums_to_one_at_full_rank(self):
        for seed, scales in ((0, [3.0, 2.0, 1.0]), (1, [5.0, 1.0, 1.0, 0.1, 0.01])):
            X = cloud(seed, scales)
            self.assertAlmostEqual(explained_variance_ratio(X, len(scales)).sum(), 1.0, places=12)
        wide = np.random.default_rng(2).normal(size=(4, 10))  # more columns than rows: at most 4 components
        self.assertAlmostEqual(explained_variance_ratio(wide, 4).sum(), 1.0, places=12)

    def test_sorted_and_between_zero_and_one(self):
        got = explained_variance_ratio(cloud(3, [1.0, 4.0, 2.0, 3.0]), 4)
        self.assertTrue(np.all(np.diff(got) <= 1e-15))
        self.assertTrue(np.all((got >= 0) & (got <= 1)))

    def test_matches_sklearn(self):
        from sklearn.decomposition import PCA

        X = cloud(4, [4.0, 3.0, 1.0, 0.5, 0.2, 0.1], n=200)
        for k in (1, 3, 6):
            np.testing.assert_allclose(explained_variance_ratio(X, k), PCA().fit(X).explained_variance_ratio_[:k], atol=1e-9)

    def test_centers_and_ignores_overall_scale(self):
        X = cloud(5, [3.0, 1.0, 0.5])
        base = explained_variance_ratio(X, 3)
        np.testing.assert_allclose(explained_variance_ratio(X + 1000.0, 3), base, atol=1e-9)
        np.testing.assert_allclose(explained_variance_ratio(X * 7.0, 3), base, atol=1e-12)

    def test_rejects_bad_input(self):
        X = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 1.0], [2.0, 1.0]])
        with self.assertRaises(ValueError):
            explained_variance_ratio(X, 3)
        with self.assertRaises(ValueError):
            explained_variance_ratio(X, 0)
        with self.assertRaises(ValueError):
            explained_variance_ratio(X[:, 0], 1)
        with self.assertRaises(ValueError):
            explained_variance_ratio(np.ones((5, 2)), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
