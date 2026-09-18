import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import affine_lists, affine_numpy

X = [[1, 2], [3, 4], [5, 6]]
W = [[1, 0, -1], [2, 1, 0]]
B = [10, 20, 30]
EXPECTED = [[15, 22, 29], [21, 24, 27], [27, 26, 25]]


class TestAffineBatch(unittest.TestCase):
    def test_lists_small(self):
        assert_allclose(affine_lists(X, W, B), EXPECTED)

    def test_numpy_small(self):
        out = affine_numpy(np.array(X, float), np.array(W, float), np.array(B, float))
        self.assertEqual(out.shape, (3, 3))
        assert_allclose(out, EXPECTED)

    def test_lists_shape_errors(self):
        with self.assertRaises(ValueError):
            affine_lists([[1, 2, 3]], W, B)
        with self.assertRaises(ValueError):
            affine_lists(X, W, [1, 2])

    def test_numpy_shape_errors(self):
        Xa, Wa = np.array(X, float), np.array(W, float)
        with self.assertRaises(ValueError):
            affine_numpy(np.ones((3, 3)), Wa, np.array(B, float))
        with self.assertRaises(ValueError):
            affine_numpy(Xa, Wa, np.array([1.0, 2.0]))
        with self.assertRaises(ValueError):
            affine_numpy(Xa, Wa, np.array(B, float).reshape(3, 1))

    def test_inputs_unchanged(self):
        Xa, Wa, ba = np.array(X, float), np.array(W, float), np.array(B, float)
        affine_numpy(Xa, Wa, ba)
        assert_allclose(Xa, X)
        assert_allclose(Wa, W)
        Xl = [row[:] for row in X]
        affine_lists(Xl, W, B)
        self.assertEqual(Xl, X)

    def test_bias_reaches_every_row(self):
        out = affine_numpy(np.zeros((4, 2)), np.zeros((2, 3)), np.array([1.0, 2.0, 3.0]))
        assert_allclose(out, np.tile([1.0, 2.0, 3.0], (4, 1)))

    def test_versions_agree_on_random_data(self):
        rng = np.random.default_rng(0)
        for n, d, k in [(5, 3, 2), (1, 7, 4), (60, 20, 10)]:
            Xa, Wa, ba = rng.normal(size=(n, d)), rng.normal(size=(d, k)), rng.normal(size=k)
            expected = Xa @ Wa + ba
            assert_allclose(affine_numpy(Xa, Wa, ba), expected, atol=1e-9)
            assert_allclose(affine_lists(Xa.tolist(), Wa.tolist(), ba.tolist()), expected, atol=1e-9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
