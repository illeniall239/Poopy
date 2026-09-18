import math
import time
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import pairwise_distances


def loop_version(a, b):
    out = np.zeros((len(a), len(b)))
    for i in range(len(a)):
        for j in range(len(b)):
            out[i, j] = math.sqrt(sum((a[i, k] - b[j, k]) ** 2 for k in range(a.shape[1])))
    return out


class TestPairwiseDistances(unittest.TestCase):
    def test_small_example(self):
        a = np.array([[0.0, 0.0], [1.0, 1.0]])
        b = np.array([[3.0, 4.0], [0.0, 0.0], [1.0, 1.0]])
        expected = [[5.0, 0.0, math.sqrt(2)], [math.sqrt(13), math.sqrt(2), 0.0]]
        assert_allclose(pairwise_distances(a, b), expected, atol=1e-9)

    def test_output_shape_is_n_by_m(self):
        rng = np.random.default_rng(0)
        d = pairwise_distances(rng.random((5, 4)), rng.random((7, 4)))
        self.assertEqual(d.shape, (5, 7))

    def test_single_points(self):
        assert_allclose(pairwise_distances(np.array([[1.0]]), np.array([[4.0]])), [[3.0]])

    def test_distance_to_itself_is_zero_and_symmetric(self):
        rng = np.random.default_rng(1)
        a = rng.random((30, 3)) * 100
        d = pairwise_distances(a, a)
        assert_allclose(np.diag(d), np.zeros(30), atol=1e-5)
        assert_allclose(d, d.T, atol=1e-9)
        self.assertTrue((d >= 0).all())

    def test_dimension_mismatch_raises(self):
        with self.assertRaises(ValueError):
            pairwise_distances(np.zeros((2, 3)), np.zeros((4, 2)))

    def test_matches_loop_version(self):
        rng = np.random.default_rng(2)
        a = rng.normal(size=(40, 5)) * 50
        b = rng.normal(size=(25, 5)) * 50
        assert_allclose(pairwise_distances(a, b), loop_version(a, b), atol=1e-5)

    def test_2000_by_2000_is_fast(self):
        rng = np.random.default_rng(3)
        a = rng.random((2000, 3)) * 1000
        b = rng.random((2000, 3)) * 1000
        start = time.perf_counter()
        d = pairwise_distances(a, b)
        self.assertLess(time.perf_counter() - start, 1.5)
        self.assertEqual(d.shape, (2000, 2000))
        assert_allclose(d[:3, :3], loop_version(a[:3], b[:3]), atol=1e-5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
