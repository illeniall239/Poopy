import math
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import predict, softmax_loss_and_grad, train_softmax_regression

STRICT = dict(over="raise", divide="raise", invalid="raise")


def three_blobs(seed, per_class=150):
    rng = np.random.default_rng(seed)
    centers = np.array([[0.0, 3.0], [-3.0, -2.0], [3.0, -2.0]])
    X = np.vstack([rng.normal(c, 1.0, size=(per_class, 2)) for c in centers])
    y = np.repeat(np.arange(3), per_class)
    return X, y


class TestSoftmaxRegression(unittest.TestCase):
    def test_hand_example(self):
        X = np.array([[1.0, 0.0], [0.0, 1.0]])
        loss, dW, db = softmax_loss_and_grad(X, np.array([0, 1]), np.zeros((2, 2)), np.zeros(2))
        self.assertAlmostEqual(loss, math.log(2), places=12)
        self.assertIsInstance(loss, float)
        assert_allclose(dW, [[-0.25, 0.25], [0.25, -0.25]], atol=1e-12)
        assert_allclose(db, [0.0, 0.0], atol=1e-12)

    def test_gradient_matches_finite_differences(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(20, 3))
        y = rng.integers(0, 4, size=20)
        W = rng.normal(size=(3, 4))
        b = rng.normal(size=4)
        _, dW, db = softmax_loss_and_grad(X, y, W, b)
        self.assertEqual(dW.shape, (3, 4))
        self.assertEqual(db.shape, (4,))
        h = 1e-6
        num_W = np.zeros_like(W)
        for idx in np.ndindex(W.shape):
            Wp, Wm = W.copy(), W.copy()
            Wp[idx] += h
            Wm[idx] -= h
            num_W[idx] = (softmax_loss_and_grad(X, y, Wp, b)[0] - softmax_loss_and_grad(X, y, Wm, b)[0]) / (2 * h)
        num_b = np.zeros_like(b)
        for i in range(4):
            bp, bm = b.copy(), b.copy()
            bp[i] += h
            bm[i] -= h
            num_b[i] = (softmax_loss_and_grad(X, y, W, bp)[0] - softmax_loss_and_grad(X, y, W, bm)[0]) / (2 * h)
        assert_allclose(dW, num_W, atol=1e-6)
        assert_allclose(db, num_b, atol=1e-6)

    def test_loss_matches_naive_on_moderate_values(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(30, 2))
        y = rng.integers(0, 3, size=30)
        W = rng.normal(size=(2, 3))
        b = rng.normal(size=3)
        Z = X @ W + b
        P = np.exp(Z) / np.exp(Z).sum(axis=1, keepdims=True)
        expected = -np.mean(np.log(P[np.arange(30), y]))
        self.assertAlmostEqual(softmax_loss_and_grad(X, y, W, b)[0], expected, places=10)

    def test_trains_three_blobs(self):
        X, y = three_blobs(2)
        W, b, losses = train_softmax_regression(X, y, 3, 0.1, 300)
        self.assertEqual(W.shape, (2, 3))
        self.assertEqual(b.shape, (3,))
        self.assertEqual(len(losses), 300)
        self.assertAlmostEqual(losses[0], math.log(3), places=12)
        for a, c in zip(losses, losses[1:]):
            self.assertLessEqual(c, a + 1e-12)
        self.assertGreater(np.mean(predict(X, W, b) == y), 0.9)
        X_new, y_new = three_blobs(3)
        self.assertGreater(np.mean(predict(X_new, W, b) == y_new), 0.9)

    def test_large_features_do_not_overflow(self):
        X, y = three_blobs(4)
        X = X * 1000.0
        with np.errstate(**STRICT):
            W, b, losses = train_softmax_regression(X, y, 3, 1e-4, 100)
            pred = predict(X, W, b)
        self.assertTrue(np.all(np.isfinite(losses)))
        self.assertGreater(np.mean(pred == y), 0.85)
        with np.errstate(**STRICT):
            loss, dW, db = softmax_loss_and_grad(np.array([[1000.0]]), np.array([1]), np.array([[1.0, 0.0]]), np.zeros(2))
        self.assertAlmostEqual(loss, 1000.0, places=9)
        assert_allclose(dW, [[1000.0, -1000.0]], atol=1e-9)

    def test_predict_is_argmax_of_logits(self):
        X = np.array([[1.0, 2.0], [-1.0, 0.5]])
        W = np.array([[1.0, -1.0, 0.0], [0.0, 2.0, 1.0]])
        b = np.array([0.0, 0.0, 0.5])
        np.testing.assert_array_equal(predict(X, W, b), np.argmax(X @ W + b, axis=1))

    def test_rejects_bad_input(self):
        X, y = three_blobs(5, per_class=5)
        with self.assertRaises(ValueError):
            train_softmax_regression(X, y, 3, 0.0, 10)
        with self.assertRaises(ValueError):
            train_softmax_regression(X, y, 3, 0.1, 0)
        with self.assertRaises(ValueError):
            train_softmax_regression(X, y, 2, 0.1, 10)
        with self.assertRaises(ValueError):
            train_softmax_regression(X, y[:-1], 3, 0.1, 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
