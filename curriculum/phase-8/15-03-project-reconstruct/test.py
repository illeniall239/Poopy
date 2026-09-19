import unittest

import numpy as np

from solution import project, reconstruct

RECT = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 1.0], [2.0, 1.0]])


def cloud(seed, scales, n=300, offset=0.0):
    rng = np.random.default_rng(seed)
    d = len(scales)
    q, _ = np.linalg.qr(rng.normal(size=(d, d)))
    return (rng.normal(size=(n, d)) * np.array(scales)) @ q.T + offset


def cov_eigenvalues_desc(X):
    return np.linalg.eigvalsh(np.cov(X, rowvar=False))[::-1]


class TestProjectReconstruct(unittest.TestCase):
    def test_rectangle_by_hand(self):
        Z, components, mean = project(RECT, 1)
        self.assertEqual(Z.shape, (4, 1))
        self.assertEqual(components.shape, (1, 2))
        np.testing.assert_allclose(mean, [1.0, 0.5], atol=1e-12)
        np.testing.assert_allclose(np.abs(components), [[1.0, 0.0]], atol=1e-12)
        np.testing.assert_allclose(np.abs(Z[:, 0]), [1.0, 1.0, 1.0, 1.0], atol=1e-12)
        back = reconstruct(Z, components, mean)
        np.testing.assert_allclose(back, [[0.0, 0.5], [2.0, 0.5], [0.0, 0.5], [2.0, 0.5]], atol=1e-12)

    def test_full_rank_round_trip_is_exact(self):
        X = cloud(0, [3.0, 2.0, 1.0, 0.5], offset=10.0)
        np.testing.assert_allclose(reconstruct(*project(X, 4)), X, atol=1e-9)

    def test_error_equals_dropped_variance(self):
        X = cloud(1, [4.0, 2.0, 1.0, 0.5, 0.25], offset=-3.0)
        eig = cov_eigenvalues_desc(X)
        for k in range(1, 6):
            back = reconstruct(*project(X, k))
            error = ((X - back) ** 2).sum() / (len(X) - 1)
            self.assertAlmostEqual(error, eig[k:].sum(), places=9)

    def test_components_orthonormal_and_mean(self):
        X = cloud(2, [3.0, 1.0, 0.5], offset=5.0)
        Z, components, mean = project(X, 2)
        np.testing.assert_allclose(components @ components.T, np.eye(2), atol=1e-12)
        np.testing.assert_allclose(mean, X.mean(axis=0), atol=1e-12)

    def test_z_columns_are_uncorrelated_with_eigenvalue_variances(self):
        X = cloud(3, [5.0, 2.0, 1.0, 0.3])
        Z, _, _ = project(X, 3)
        cov_z = np.cov(Z, rowvar=False)
        np.testing.assert_allclose(np.diag(cov_z), cov_eigenvalues_desc(X)[:3], atol=1e-9)
        np.testing.assert_allclose(cov_z - np.diag(np.diag(cov_z)), 0.0, atol=1e-9)

    def test_matches_sklearn_up_to_sign(self):
        from sklearn.decomposition import PCA

        X = cloud(4, [4.0, 3.0, 1.0, 0.5, 0.1], offset=2.0)
        Z, components, _ = project(X, 3)
        ref = PCA(n_components=3).fit(X)
        Z_ref = ref.transform(X)
        for i in range(3):
            sign = np.sign(Z[:, i] @ Z_ref[:, i])
            np.testing.assert_allclose(Z[:, i], sign * Z_ref[:, i], atol=1e-9)
            np.testing.assert_allclose(components[i], sign * ref.components_[i], atol=1e-9)

    def test_reconstruct_takes_any_coordinates(self):
        components = np.array([[0.6, 0.8]])
        mean = np.array([1.0, 1.0])
        np.testing.assert_allclose(reconstruct(np.array([[5.0], [0.0]]), components, mean), [[4.0, 5.0], [1.0, 1.0]], atol=1e-12)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            project(RECT, 3)
        with self.assertRaises(ValueError):
            project(RECT, 0)
        with self.assertRaises(ValueError):
            project(RECT[:, 0], 1)
        Z, components, mean = project(RECT, 1)
        with self.assertRaises(ValueError):
            reconstruct(Z, np.eye(2), mean)
        with self.assertRaises(ValueError):
            reconstruct(Z, components, np.zeros(3))
        with self.assertRaises(ValueError):
            reconstruct(Z[:, 0], components, mean)


if __name__ == "__main__":
    unittest.main(verbosity=2)
