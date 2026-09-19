import unittest

import numpy as np
from sklearn.decomposition import PCA

from solution import reconstruction_errors, top_anomalies


def correlated_data(seed, n=400):
    """Three features driven by one hidden factor, plus small noise."""
    rng = np.random.default_rng(seed)
    t = rng.normal(size=n)
    noise = rng.normal(scale=0.1, size=(n, 3))
    return np.column_stack([t, 2 * t, -t]) + noise


class TestReconstructionAnomaly(unittest.TestCase):
    def test_hand_computed_line(self):
        X_train = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])
        errs = reconstruction_errors(X_train, np.array([[5.0, 5.0], [1.0, 2.0]]), 1)
        self.assertEqual(errs.shape, (2,))
        np.testing.assert_allclose(errs, [0.0, 0.5], atol=1e-9)

    def test_all_components_reconstruct_exactly(self):
        X = correlated_data(0)
        errs = reconstruction_errors(X, X[:50] + 3.0, 3)
        np.testing.assert_allclose(errs, np.zeros(50), atol=1e-9)

    def test_matches_sklearn_pca(self):
        X = correlated_data(1)
        new = correlated_data(2, n=30) + np.random.default_rng(3).normal(scale=0.5, size=(30, 3))
        for k in (1, 2):
            pca = PCA(n_components=k).fit(X)
            expected = np.sum((new - pca.inverse_transform(pca.transform(new))) ** 2, axis=1)
            np.testing.assert_allclose(reconstruction_errors(X, new, k), expected, atol=1e-6)

    def test_centers_with_the_training_mean(self):
        X = correlated_data(4) + np.array([10.0, -5.0, 3.0])
        pca = PCA(n_components=1).fit(X)
        row = np.array([[11.0, -3.0, 2.0]])
        expected = np.sum((row - pca.inverse_transform(pca.transform(row))) ** 2)
        self.assertAlmostEqual(float(reconstruction_errors(X, row, 1)[0]), float(expected), places=6)

    def test_planted_multivariate_anomalies_rank_first(self):
        X = correlated_data(5)
        anomalies = np.array([[1.0, -2.0, 1.0], [-1.0, 2.0, -1.0], [0.8, 1.6, 0.8], [0.0, 1.5, 0.0]])
        # Every anomaly feature is inside the training range: no per-feature rule can flag it.
        z = np.abs((anomalies - X.mean(axis=0)) / X.std(axis=0))
        self.assertTrue(np.all(z < 2.0))
        rows = np.vstack([X, anomalies])
        errs = reconstruction_errors(X, rows, 1)
        self.assertEqual(sorted(top_anomalies(errs, 4)), [400, 401, 402, 403])

    def test_top_anomalies_order_and_ties(self):
        self.assertEqual(top_anomalies(np.array([0.1, 0.5, 0.2, 0.5]), 3), [1, 3, 2])
        self.assertEqual(top_anomalies(np.array([0.1, 0.5]), 10), [1, 0])
        self.assertEqual(top_anomalies(np.array([0.3, 0.3, 0.3]), 2), [0, 1])

    def test_rejects_bad_input(self):
        X = correlated_data(6)
        with self.assertRaises(ValueError):
            reconstruction_errors(X, X, 0)
        with self.assertRaises(ValueError):
            reconstruction_errors(X, X, 4)
        with self.assertRaises(ValueError):
            reconstruction_errors(X, X[:, :2], 1)
        with self.assertRaises(ValueError):
            reconstruction_errors(X, X[0], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
