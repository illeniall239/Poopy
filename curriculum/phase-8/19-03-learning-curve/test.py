import unittest

import numpy as np

from solution import learning_curve, more_data_helps


def mean_fit(X, y):
    return float(np.mean(y))


def mean_predict(model, X):
    return np.full(len(X), model)


def noisy_sine(seed=0, n=600):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1, 1, n)
    y = np.sin(3 * x) + rng.normal(0, 0.3, n)
    perm = rng.permutation(n)
    folds = [(perm[:400].tolist(), perm[400:].tolist()), (perm[200:].tolist(), perm[:200].tolist())]
    return x[:, None], y, folds


def poly(degree):
    return lambda X, y: np.polyfit(X[:, 0], y, degree)


def poly_predict(model, X):
    return np.polyval(model, X[:, 0])


class TestLearningCurve(unittest.TestCase):
    def test_hand_computed_mean_model(self):
        X = np.arange(6)[:, None]
        y = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0])
        curve = learning_curve(mean_fit, mean_predict, X, y, [2, 4], [([0, 1, 2, 3], [4, 5])])
        self.assertEqual([s for s, _, _ in curve], [2, 4])
        np.testing.assert_allclose([t for _, t, _ in curve], [1.0, 5.0])
        np.testing.assert_allclose([v for _, _, v in curve], [65.0, 37.0])

    def test_averages_over_folds(self):
        X = np.arange(6)[:, None]
        y = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0])
        folds = [([0, 1, 2, 3], [4, 5]), ([5, 4, 3, 2], [0, 1])]
        # Fold 2, size 2: mean 9, train error 1, val error (81 + 49) / 2 = 65.
        (s, train, val), = learning_curve(mean_fit, mean_predict, X, y, [2], folds)
        self.assertEqual(s, 2)
        self.assertAlmostEqual(train, 1.0)
        self.assertAlmostEqual(val, 65.0)

    def test_trains_on_the_first_s_training_rows_only(self):
        X = np.arange(20)[:, None].astype(float)
        y = np.zeros(20)
        seen = []

        def spy_fit(Xs, ys):
            seen.append(Xs[:, 0].astype(int).tolist())
            return 0.0

        folds = [(list(range(10, 20)), list(range(10))), (list(range(9, -1, -1)), list(range(10, 20)))]
        learning_curve(spy_fit, mean_predict, X, y, [3, 10], folds)
        self.assertEqual(seen, [[10, 11, 12], [9, 8, 7], list(range(10, 20)), list(range(9, -1, -1))])

    def test_high_variance_model_more_data_helps(self):
        X, y, folds = noisy_sine()
        curve = learning_curve(poly(9), poly_predict, X, y, [15, 30, 60], folds)
        gaps = [v - t for _, t, v in curve]
        self.assertGreater(gaps[0], gaps[1])
        self.assertGreater(gaps[1], gaps[2])
        self.assertTrue(more_data_helps(curve, tol=0.005))

    def test_high_bias_model_more_data_does_not_help(self):
        X, y, folds = noisy_sine()
        curve = learning_curve(poly(1), poly_predict, X, y, [15, 30, 60], folds)
        self.assertGreater(curve[-1][1], 0.2)  # training error itself is high
        self.assertFalse(more_data_helps(curve, tol=0.005))

    def test_more_data_helps_on_hand_curves(self):
        closing = [(10, 0.05, 0.60), (20, 0.08, 0.40), (40, 0.10, 0.30)]
        closed = [(10, 0.05, 0.60), (20, 0.20, 0.25), (40, 0.22, 0.2205)]
        flat = [(10, 0.10, 0.30), (20, 0.10, 0.30), (40, 0.10, 0.30)]
        widening = [(10, 0.10, 0.20), (20, 0.10, 0.30)]
        self.assertTrue(more_data_helps(closing))
        self.assertFalse(more_data_helps(closed))
        self.assertFalse(more_data_helps(flat))
        self.assertFalse(more_data_helps(widening))
        self.assertTrue(more_data_helps(closing, tol=0.05))
        self.assertFalse(more_data_helps(closing, tol=0.25))

    def test_rejects_bad_input(self):
        X = np.arange(6)[:, None]
        y = np.arange(6, dtype=float)
        folds = [([0, 1, 2, 3], [4, 5])]
        with self.assertRaises(ValueError):
            learning_curve(mean_fit, mean_predict, X, y, [5], folds)
        with self.assertRaises(ValueError):
            learning_curve(mean_fit, mean_predict, X, y, [0], folds)
        with self.assertRaises(ValueError):
            learning_curve(mean_fit, mean_predict, X, y, [], folds)
        with self.assertRaises(ValueError):
            more_data_helps([(10, 0.1, 0.3)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
