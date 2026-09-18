import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import center, covariance_matrix


class TestCovarianceMatrix(unittest.TestCase):
    def test_center(self):
        assert_allclose(center([[1, 2], [3, 6], [5, 10]]), [[-2, -4], [0, 0], [2, 4]])
        rows = [[1, 2], [3, 4]]
        center(rows)
        self.assertEqual(rows, [[1, 2], [3, 4]])

    def test_small_examples(self):
        assert_allclose(covariance_matrix([[1, 2], [3, 6], [5, 10]]), [[4.0, 8.0], [8.0, 16.0]])
        assert_allclose(covariance_matrix([[1, 2], [3, 6], [5, 10]], 0), [[8 / 3, 16 / 3], [16 / 3, 32 / 3]])
        assert_allclose(covariance_matrix([[1, 0], [0, 1], [-1, 0], [0, -1]]), [[2 / 3, 0.0], [0.0, 2 / 3]])

    def test_errors(self):
        with self.assertRaises(ValueError):
            covariance_matrix([[1, 2]])
        with self.assertRaises(ValueError):
            covariance_matrix([])
        with self.assertRaises(ValueError):
            covariance_matrix([[1, 2], [3]])
        with self.assertRaises(ValueError):
            center([])

    def test_uncentered_data_same_covariance(self):
        rows = [[1, 2], [3, 6], [5, 10]]
        shifted = [[a + 100, b - 50] for a, b in rows]
        assert_allclose(covariance_matrix(shifted), covariance_matrix(rows), atol=1e-9)

    def test_symmetric_with_variances_on_diagonal(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=(50, 4))
        c = np.array(covariance_matrix(x.tolist()))
        assert_allclose(c, c.T)
        assert_allclose(np.diag(c), x.var(axis=0, ddof=1), atol=1e-9)

    def test_matches_numpy_random(self):
        rng = np.random.default_rng(1)
        for n, d in [(5, 2), (100, 6), (2000, 10)]:
            x = rng.normal(size=(n, d)) @ rng.normal(size=(d, d)) + 10
            for ddof in (0, 1):
                assert_allclose(covariance_matrix(x.tolist(), ddof), np.cov(x, rowvar=False, ddof=ddof), atol=1e-9)

    def test_single_feature(self):
        assert_allclose(covariance_matrix([[1.0], [2.0], [3.0]]), [[1.0]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
