import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import power_iteration, top_two_eigenpairs


def spectral(eigenvalues, seed):
    rng = np.random.default_rng(seed)
    q, _ = np.linalg.qr(rng.normal(size=(len(eigenvalues), len(eigenvalues))))
    return q @ np.diag(eigenvalues) @ q.T


class TestPowerIteration(unittest.TestCase):
    def test_diagonal(self):
        lam, v = power_iteration(np.array([[2.0, 0.0], [0.0, 1.0]]))
        self.assertAlmostEqual(lam, 2.0, places=9)
        self.assertAlmostEqual(abs(v[0]), 1.0, places=6)
        self.assertAlmostEqual(v[1], 0.0, places=6)

    def test_two_by_two(self):
        A = np.array([[2.0, 1.0], [1.0, 2.0]])
        lam, v = power_iteration(A)
        self.assertAlmostEqual(lam, 3.0, places=9)
        self.assertAlmostEqual(abs(v @ np.array([1, 1]) / np.sqrt(2)), 1.0, places=9)
        self.assertAlmostEqual(np.linalg.norm(v), 1.0, places=12)

    def test_eigen_equation_holds(self):
        A = spectral([10.0, 4.0, 1.0, 0.5], seed=0)
        lam, v = power_iteration(A)
        assert_allclose(A @ v, lam * v, atol=1e-6)

    def test_matches_numpy_up_to_sign(self):
        for seed, eigs in [(1, [10.0, 4.0, 1.0, 0.5]), (2, [7.0, 3.0, 2.9, 0.1, 0.0]), (3, list(range(30, 0, -1)))]:
            A = spectral(eigs, seed)
            w, U = np.linalg.eigh(A)
            lam, v = power_iteration(A)
            self.assertAlmostEqual(lam, w[-1], places=6)
            self.assertGreater(abs(v @ U[:, -1]), 1 - 1e-6)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            power_iteration(np.array([[1.0, 2.0], [0.0, 1.0]]))
        with self.assertRaises(ValueError):
            power_iteration(np.ones((2, 3)))
        with self.assertRaises(ValueError):
            power_iteration(np.ones(3))

    def test_top_two_with_deflation(self):
        A = np.array([[2.0, 1.0], [1.0, 2.0]])
        (l1, v1), (l2, v2) = top_two_eigenpairs(A)
        self.assertAlmostEqual(l1, 3.0, places=8)
        self.assertAlmostEqual(l2, 1.0, places=8)
        self.assertAlmostEqual(abs(v2 @ np.array([1, -1]) / np.sqrt(2)), 1.0, places=6)
        self.assertAlmostEqual(v1 @ v2, 0.0, places=6)

    def test_top_two_matches_numpy(self):
        A = spectral([10.0, 4.0, 1.0, 0.5], seed=5)
        w, U = np.linalg.eigh(A)
        (l1, v1), (l2, v2) = top_two_eigenpairs(A)
        self.assertAlmostEqual(l1, 10.0, places=6)
        self.assertAlmostEqual(l2, 4.0, places=6)
        self.assertGreater(abs(v1 @ U[:, -1]), 1 - 1e-6)
        self.assertGreater(abs(v2 @ U[:, -2]), 1 - 1e-6)

    def test_covariance_of_stretched_cloud(self):
        rng = np.random.default_rng(7)
        x = rng.normal(size=(500, 2)) * np.array([5.0, 1.0])
        theta = 0.6
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        x = x @ rot.T
        cov = np.cov(x, rowvar=False)
        lam, v = power_iteration(cov)
        self.assertGreater(abs(v @ rot[:, 0]), 0.99)
        self.assertGreater(lam, 20.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
