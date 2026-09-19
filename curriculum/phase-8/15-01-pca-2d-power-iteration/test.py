import unittest

import numpy as np

from solution import pca_2d


def stretched(seed, scales, n=500, offset=0.0):
    rng = np.random.default_rng(seed)
    d = len(scales)
    q, _ = np.linalg.qr(rng.normal(size=(d, d)))
    return (rng.normal(size=(n, d)) * np.array(scales)) @ q.T + offset


def numpy_top_two(points):
    w, U = np.linalg.eigh(np.cov(points, rowvar=False))
    return w[::-1][:2], U[:, ::-1][:, :2].T


class TestPCA2D(unittest.TestCase):
    def assertMatchesNumpy(self, points):
        components, variances = pca_2d(points)
        w, U = numpy_top_two(points)
        self.assertEqual(components.shape, (2, points.shape[1]))
        self.assertEqual(variances.shape, (2,))
        np.testing.assert_allclose(variances, w, rtol=0, atol=1e-6)
        for i in range(2):
            self.assertGreater(abs(components[i] @ U[i]), 1 - 1e-6)

    def test_two_dimensional_rotated_cloud(self):
        rng = np.random.default_rng(7)
        theta = 0.6
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        points = (rng.normal(size=(500, 2)) * np.array([5.0, 1.0])) @ rot.T
        components, variances = pca_2d(points)
        self.assertGreater(abs(components[0] @ rot[:, 0]), 0.99)
        self.assertGreater(abs(components[1] @ rot[:, 1]), 0.99)
        self.assertGreater(variances[0], 10 * variances[1])
        self.assertMatchesNumpy(points)

    def test_matches_numpy_up_to_sign(self):
        for seed, scales in ((0, [4.0, 2.0, 1.0]), (1, [6.0, 3.0, 1.5, 1.0, 0.5]), (2, [3.0, 2.0, 1.0, 1.0, 0.2, 0.1])):
            self.assertMatchesNumpy(stretched(seed, scales))

    def test_components_are_orthonormal(self):
        components, _ = pca_2d(stretched(3, [5.0, 2.0, 1.0, 0.5]))
        np.testing.assert_allclose(components @ components.T, np.eye(2), atol=1e-6)

    def test_centers_the_data(self):
        points = stretched(4, [3.0, 1.0, 0.3], offset=100.0)
        self.assertMatchesNumpy(points)
        c_far, v_far = pca_2d(points)
        c_near, v_near = pca_2d(points - 100.0)
        np.testing.assert_allclose(v_far, v_near, atol=1e-6)
        for i in range(2):
            self.assertGreater(abs(c_far[i] @ c_near[i]), 1 - 1e-6)

    def test_uses_the_sample_covariance(self):
        points = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 1.0], [2.0, 1.0]])
        components, variances = pca_2d(points)
        # column variances with n - 1: 4/3 and 1/3; the axes are the components
        np.testing.assert_allclose(variances, [4 / 3, 1 / 3], atol=1e-9)
        self.assertAlmostEqual(abs(components[0][0]), 1.0, places=6)
        self.assertAlmostEqual(abs(components[1][1]), 1.0, places=6)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            pca_2d(np.zeros(5))
        with self.assertRaises(ValueError):
            pca_2d(np.zeros((1, 3)))
        with self.assertRaises(ValueError):
            pca_2d(np.zeros((5, 1)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
