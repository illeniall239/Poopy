import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import explained_variance, low_rank, reconstruction_error


class TestLowRankApproximation(unittest.TestCase):
    def test_diagonal_example(self):
        X = np.array([[3.0, 0.0], [0.0, 0.5]])
        assert_allclose(low_rank(X, 1), [[3.0, 0.0], [0.0, 0.0]], atol=1e-12)
        self.assertAlmostEqual(reconstruction_error(X, 1), 0.5, places=12)
        self.assertAlmostEqual(reconstruction_error(X, 2), 0.0, places=12)

    def test_rank_one_matrix_is_exact(self):
        X = np.outer([1.0, 2.0, 3.0], [4.0, 5.0])
        assert_allclose(low_rank(X, 1), X, atol=1e-9)
        self.assertAlmostEqual(reconstruction_error(X, 1), 0.0, places=9)

    def test_full_rank_reproduces_x(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(7, 4))
        assert_allclose(low_rank(X, 4), X, atol=1e-9)
        self.assertEqual(low_rank(X, 2).shape, X.shape)

    def test_k_validation(self):
        X = np.ones((3, 2))
        for k in [0, 3, -1]:
            with self.assertRaises(ValueError):
                low_rank(X, k)
            with self.assertRaises(ValueError):
                explained_variance(X, k)

    def test_error_equals_dropped_energy(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(40, 15)) @ np.diag(np.linspace(5, 0.1, 15)) @ rng.normal(size=(15, 15))
        s = np.linalg.svd(X, compute_uv=False)
        for k in [1, 3, 8, 15]:
            self.assertAlmostEqual(reconstruction_error(X, k), float(np.sqrt((s[k:] ** 2).sum())), places=9)

    def test_truncation_has_rank_k(self):
        rng = np.random.default_rng(2)
        X = rng.normal(size=(30, 10))
        for k in [1, 4]:
            self.assertEqual(np.linalg.matrix_rank(low_rank(X, k)), k)

    def test_explained_variance_on_a_line(self):
        rng = np.random.default_rng(3)
        t = rng.normal(size=200)
        rows = np.column_stack([3 * t, -t]) + rng.normal(scale=0.05, size=(200, 2)) + 100.0
        ev1 = explained_variance(rows, 1)
        self.assertGreater(ev1, 0.99)
        self.assertLess(ev1, 1.0)
        self.assertAlmostEqual(explained_variance(rows, 2), 1.0, places=12)

    def test_explained_variance_matches_covariance_eigenvalues(self):
        rng = np.random.default_rng(4)
        X = rng.normal(size=(300, 6)) @ rng.normal(size=(6, 6)) + 50.0
        w = np.sort(np.linalg.eigvalsh(np.cov(X, rowvar=False)))[::-1]
        prev = 0.0
        for k in range(1, 7):
            ev = explained_variance(X, k)
            self.assertAlmostEqual(ev, float(w[:k].sum() / w.sum()), places=9)
            self.assertGreaterEqual(ev, prev - 1e-12)
            prev = ev
        self.assertAlmostEqual(explained_variance(X, 6), 1.0, places=12)

    def test_centering_matters(self):
        rng = np.random.default_rng(5)
        X = rng.normal(size=(100, 3))
        shifted = X + np.array([1000.0, 0.0, 0.0])
        self.assertAlmostEqual(explained_variance(shifted, 1), explained_variance(X, 1), places=6)
        s_uncentered = np.linalg.svd(shifted, compute_uv=False)
        self.assertGreater(float(s_uncentered[0] ** 2 / (s_uncentered**2).sum()), 0.99)


if __name__ == "__main__":
    unittest.main(verbosity=2)
