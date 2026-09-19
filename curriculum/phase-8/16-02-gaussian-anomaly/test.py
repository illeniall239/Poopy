import unittest

import numpy as np
from scipy.stats import norm

from solution import GaussianAnomalyDetector


def planted(seed):
    rng = np.random.default_rng(seed)
    normal = rng.normal([10.0, -3.0, 0.0], [2.0, 0.5, 1.0], size=(500, 3))
    anomalies = np.array([[25.0, -3.0, 0.0], [10.0, 1.0, 0.0], [10.0, -3.0, 7.0], [-5.0, -6.0, 5.0]])
    return normal, anomalies


class TestGaussianAnomaly(unittest.TestCase):
    def test_fit_returns_self_and_uses_population_variance(self):
        X, _ = planted(0)
        d = GaussianAnomalyDetector()
        self.assertIs(d.fit(X), d)
        # At the column means the density peaks, and the peak depends only on the variance used.
        peak = d.score(X.mean(axis=0, keepdims=True))[0]
        self.assertAlmostEqual(peak, float(np.sum(-0.5 * np.log(2 * np.pi * X.var(axis=0)))), places=9)

    def test_score_hand_computed(self):
        d = GaussianAnomalyDetector().fit(np.array([[0.0], [2.0]]))
        s = d.score(np.array([[1.0], [3.0]]))
        self.assertEqual(s.shape, (2,))
        self.assertAlmostEqual(s[0], -0.5 * np.log(2 * np.pi), places=9)
        self.assertAlmostEqual(s[1], -0.5 * np.log(2 * np.pi) - 2.0, places=9)

    def test_score_matches_scipy(self):
        X, A = planted(1)
        d = GaussianAnomalyDetector().fit(X)
        rows = np.vstack([X[:20], A])
        expected = norm.logpdf(rows, X.mean(axis=0), X.std(axis=0)).sum(axis=1)
        np.testing.assert_allclose(d.score(rows), expected, atol=1e-9)

    def test_planted_anomalies_score_lowest(self):
        X, A = planted(2)
        d = GaussianAnomalyDetector().fit(X)
        s = d.score(np.vstack([X, A]))
        self.assertEqual(set(np.argsort(s)[:4].tolist()), set(range(500, 504)))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            GaussianAnomalyDetector().fit(np.array([[1.0, 5.0], [2.0, 5.0]]))
        with self.assertRaises(ValueError):
            GaussianAnomalyDetector().fit(np.array([1.0, 2.0, 3.0]))
        with self.assertRaises(RuntimeError):
            GaussianAnomalyDetector().score(np.array([[1.0]]))

    def test_choose_epsilon_hand_computed(self):
        eps, f1 = GaussianAnomalyDetector.choose_epsilon(
            np.array([-10.0, -9.0, -3.0, -2.0, -1.0, 0.0]), np.array([1, 0, 1, 0, 0, 0])
        )
        self.assertEqual(eps, -3.0)
        self.assertAlmostEqual(f1, 0.8)

    def test_choose_epsilon_ties_take_the_smallest(self):
        # eps=-5: TP=1 FP=0 FN=1, F1=2/3.  eps=-4: F1=1/2.  eps=-3: F1=2/5.  eps=-2: TP=2 FP=2, F1=2/3.
        eps, f1 = GaussianAnomalyDetector.choose_epsilon(np.array([-2.0, -5.0, -3.0, -4.0]), np.array([1, 1, 0, 0]))
        self.assertAlmostEqual(f1, 2 / 3)
        self.assertEqual(eps, -5.0)

    def test_choose_epsilon_rejects_no_anomalies_and_bad_lengths(self):
        with self.assertRaises(ValueError):
            GaussianAnomalyDetector.choose_epsilon(np.array([-1.0, -2.0]), np.array([0, 0]))
        with self.assertRaises(ValueError):
            GaussianAnomalyDetector.choose_epsilon(np.array([-1.0, -2.0]), np.array([1]))

    def test_end_to_end_validation_threshold(self):
        X, A = planted(4)
        train, val_normal = X[:400], X[400:]
        d = GaussianAnomalyDetector().fit(train)
        scores = d.score(np.vstack([val_normal, A]))
        labels = np.array([0] * len(val_normal) + [1] * len(A))
        eps, f1 = d.choose_epsilon(scores, labels)
        self.assertGreater(f1, 0.85)
        self.assertTrue(np.all(scores[labels == 1] <= eps))


if __name__ == "__main__":
    unittest.main(verbosity=2)
