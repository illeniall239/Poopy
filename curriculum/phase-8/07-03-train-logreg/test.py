import math
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import predict, predict_proba, train_logreg

STRICT = dict(over="raise", divide="raise", invalid="raise")


def blobs(seed, n=400):
    rng = np.random.default_rng(seed)
    X = np.vstack([rng.normal([-2.0, -1.0], 1.0, size=(n // 2, 2)), rng.normal([2.0, 1.0], 1.0, size=(n // 2, 2))])
    y = np.array([0] * (n // 2) + [1] * (n // 2))
    return X, y


class TestTrainLogreg(unittest.TestCase):
    def test_first_step_by_hand(self):
        X = np.array([[0.0], [1.0], [2.0], [3.0]])
        y = np.array([0, 0, 1, 1])
        w, b, losses = train_logreg(X, y, 0.5, 1)
        self.assertEqual(len(losses), 1)
        self.assertAlmostEqual(losses[0], math.log(2), places=12)
        assert_allclose(w, [0.25], atol=1e-12)
        self.assertAlmostEqual(b, 0.0, places=12)
        self.assertIsInstance(b, float)
        self.assertIsInstance(losses[0], float)

    def test_two_steps_by_hand(self):
        X = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
        y = np.array([1, 0, 1])
        w, b, losses = train_logreg(X, y, 1.0, 2)
        # step 1 from zeros: p = 0.5, error = [-0.5, 0.5, -0.5]
        e0 = np.array([-0.5, 0.5, -0.5])
        w1 = -X.T @ e0 / 3
        b1 = -e0.mean()
        p = 1 / (1 + np.exp(-(X @ w1 + b1)))
        e1 = p - y
        assert_allclose(w, w1 - X.T @ e1 / 3, atol=1e-12)
        self.assertAlmostEqual(b, b1 - e1.mean(), places=12)
        expected_loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
        self.assertAlmostEqual(losses[1], expected_loss, places=12)

    def test_separable_accuracy_and_monotone_loss(self):
        X, y = blobs(0)
        w, b, losses = train_logreg(X, y, 0.1, 500)
        self.assertEqual(len(losses), 500)
        for a, c in zip(losses, losses[1:]):
            self.assertLessEqual(c, a + 1e-12)
        self.assertGreater(np.mean(predict(X, w, b) == y), 0.95)
        self.assertLess(losses[-1], 0.2)

    def test_deterministic(self):
        X, y = blobs(1)
        w1, b1, l1 = train_logreg(X, y, 0.1, 50)
        w2, b2, l2 = train_logreg(X, y, 0.1, 50)
        assert_allclose(w1, w2)
        self.assertEqual(b1, b2)
        self.assertEqual(l1, l2)

    def test_unscaled_features_do_not_overflow(self):
        X, y = blobs(2)
        X = X * 1000.0
        with np.errstate(**STRICT):
            w, b, losses = train_logreg(X, y, 0.01, 200)
            probs = predict_proba(X, w, b)
        self.assertTrue(np.all(np.isfinite(losses)))
        self.assertTrue(np.all((probs >= 0) & (probs <= 1)))
        self.assertGreater(np.mean(predict(X, w, b) == y), 0.9)

    def test_threshold_is_a_choice(self):
        X, y = blobs(3)
        w, b, _ = train_logreg(X, y, 0.1, 300)
        probs = predict_proba(X, w, b)
        self.assertEqual(probs.shape, (len(X),))
        pred = predict(X, w, b)
        assert_allclose(pred, (probs >= 0.5).astype(int))
        strict = predict(X, w, b, threshold=0.99)
        self.assertLess(strict.sum(), pred.sum())
        self.assertTrue(set(np.unique(strict).tolist()) <= {0, 1})

    def test_rejects_bad_input(self):
        X, y = blobs(4)
        with self.assertRaises(ValueError):
            train_logreg(X, y, 0.0, 10)
        with self.assertRaises(ValueError):
            train_logreg(X, y, 0.1, 0)
        with self.assertRaises(ValueError):
            train_logreg(X, y[:-1], 0.1, 10)
        with self.assertRaises(ValueError):
            train_logreg(X[:, 0], y, 0.1, 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
