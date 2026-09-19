import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import linear_backward


def numeric_grads(X, W, b, G, h=1e-6):
    """Central differences of L = sum(G * (X @ W + b)), whose dL/dY is exactly G."""
    loss = lambda X, W, b: float(np.sum(G * (X @ W + b)))
    grads = []
    for which in range(3):
        arrs = [X, W, b]
        target = arrs[which]
        g = np.zeros_like(target)
        for idx in np.ndindex(target.shape):
            plus = [a.copy() for a in arrs]
            minus = [a.copy() for a in arrs]
            plus[which][idx] += h
            minus[which][idx] -= h
            g[idx] = (loss(*plus) - loss(*minus)) / (2 * h)
        grads.append(g)
    return grads


class TestLinearBackward(unittest.TestCase):
    def test_worked_example(self):
        W = np.array([[1.0, 0.0, 2.0], [0.0, 1.0, 3.0]])
        dX, dW, db = linear_backward(np.array([[1.0, 2.0]]), W, np.array([[1.0, 1.0, 1.0]]))
        assert_allclose(dX, [[3.0, 4.0]])
        assert_allclose(dW, [[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]])
        assert_allclose(db, [1.0, 1.0, 1.0])

    def test_shapes_match_the_inputs(self):
        rng = np.random.default_rng(0)
        X, W, dY = rng.normal(size=(5, 3)), rng.normal(size=(3, 4)), rng.normal(size=(5, 4))
        dX, dW, db = linear_backward(X, W, dY)
        self.assertEqual((dX.shape, dW.shape, db.shape), ((5, 3), (3, 4), (4,)))

    def test_matches_finite_differences_rectangular(self):
        rng = np.random.default_rng(1)
        X, W, b = rng.normal(size=(4, 3)), rng.normal(size=(3, 2)), rng.normal(size=2)
        G = rng.normal(size=(4, 2))
        dX, dW, db = linear_backward(X, W, G)
        nX, nW, nb = numeric_grads(X, W, b, G)
        assert_allclose(dX, nX, atol=1e-6)
        assert_allclose(dW, nW, atol=1e-6)
        assert_allclose(db, nb, atol=1e-6)

    def test_square_weights_catch_a_missing_transpose(self):
        rng = np.random.default_rng(2)
        X, W, b = rng.normal(size=(3, 3)), rng.normal(size=(3, 3)), rng.normal(size=3)
        G = rng.normal(size=(3, 3))
        dX, dW, db = linear_backward(X, W, G)
        nX, nW, nb = numeric_grads(X, W, b, G)
        assert_allclose(dX, nX, atol=1e-6)
        assert_allclose(dW, nW, atol=1e-6)

    def test_bias_gradient_sums_over_the_batch(self):
        dY = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        _, _, db = linear_backward(np.ones((3, 2)), np.ones((2, 2)), dY)
        self.assertEqual(db.shape, (2,))
        assert_allclose(db, [9.0, 12.0])

    def test_inputs_are_not_modified(self):
        rng = np.random.default_rng(3)
        X, W, dY = rng.normal(size=(2, 3)), rng.normal(size=(3, 2)), rng.normal(size=(2, 2))
        copies = (X.copy(), W.copy(), dY.copy())
        linear_backward(X, W, dY)
        for before, after in zip(copies, (X, W, dY)):
            assert_allclose(after, before)

    def test_rejects_bad_shapes(self):
        with self.assertRaises(ValueError):
            linear_backward(np.ones((2, 3)), np.ones((4, 2)), np.ones((2, 2)))
        with self.assertRaises(ValueError):
            linear_backward(np.ones((2, 3)), np.ones((3, 2)), np.ones((3, 2)))
        with self.assertRaises(ValueError):
            linear_backward(np.ones(3), np.ones((3, 2)), np.ones((1, 2)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
