import unittest

import numpy as np

from solution import permutation_importance


def neg_mse(t, p):
    return -float(np.mean((t - p) ** 2))


def accuracy(t, p):
    return float(np.mean(t == p))


def replay(predict, X, y, metric, seed, repeats):
    rng = np.random.default_rng(seed)
    base = metric(y, predict(X))
    out = []
    for j in range(X.shape[1]):
        drops = []
        for _ in range(repeats):
            Xp = X.copy()
            Xp[:, j] = rng.permutation(X[:, j])
            drops.append(base - metric(y, predict(Xp)))
        out.append(np.mean(drops))
    return np.array(out)


def linear_setup():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(300, 3))
    w = np.array([3.0, 1.0, 0.0])
    return X, X @ w, (lambda A: A @ w)


class TestPermutationImportance(unittest.TestCase):
    def test_ignored_feature_is_exactly_zero(self):
        X = np.array([[1.0, 5.0], [2.0, 5.0], [3.0, 7.0], [4.0, 7.0]])
        y = X[:, 0] * 2
        imp = permutation_importance(lambda A: A[:, 0] * 2, X, y, neg_mse, np.random.default_rng(0), repeats=3)
        self.assertEqual(imp.shape, (2,))
        self.assertGreater(imp[0], 0.0)
        self.assertEqual(imp[1], 0.0)

    def test_ranks_features_by_weight(self):
        X, y, predict = linear_setup()
        imp = permutation_importance(predict, X, y, neg_mse, np.random.default_rng(0), repeats=5)
        self.assertGreater(imp[0], imp[1])
        self.assertGreater(imp[1], 0.0)
        self.assertEqual(imp[2], 0.0)
        # Shuffling a standard-normal column with weight w adds about 2 w^2 to the MSE.
        self.assertAlmostEqual(imp[0], 18.0, delta=3.0)
        self.assertAlmostEqual(imp[1], 2.0, delta=0.4)

    def test_matches_the_pinned_replay(self):
        X, y, predict = linear_setup()
        for seed, repeats in ((0, 1), (7, 4)):
            got = permutation_importance(predict, X, y, neg_mse, np.random.default_rng(seed), repeats=repeats)
            np.testing.assert_allclose(got, replay(predict, X, y, neg_mse, seed, repeats), rtol=0, atol=1e-12)

    def test_same_seed_same_answer(self):
        X, y, predict = linear_setup()
        a = permutation_importance(predict, X, y, neg_mse, np.random.default_rng(3), repeats=3)
        b = permutation_importance(predict, X, y, neg_mse, np.random.default_rng(3), repeats=3)
        np.testing.assert_array_equal(a, b)

    def test_does_not_modify_X(self):
        X, y, predict = linear_setup()
        before = X.copy()
        permutation_importance(predict, X, y, neg_mse, np.random.default_rng(0), repeats=2)
        np.testing.assert_array_equal(X, before)

    def test_works_with_a_classifier_and_accuracy(self):
        rng = np.random.default_rng(4)
        X = rng.normal(size=(400, 2))
        y = (X[:, 1] > 0).astype(int)
        predict = lambda A: (A[:, 1] > 0).astype(int)
        imp = permutation_importance(predict, X, y, accuracy, np.random.default_rng(0), repeats=10)
        self.assertEqual(imp[0], 0.0)
        self.assertAlmostEqual(imp[1], 0.5, delta=0.06)

    def test_duplicate_column_the_model_ignores_gets_zero(self):
        rng = np.random.default_rng(5)
        x = rng.normal(size=200)
        X = np.column_stack([x, x])  # two identical, equally informative columns
        y = 2 * x
        imp = permutation_importance(lambda A: 2 * A[:, 0], X, y, neg_mse, np.random.default_rng(0), repeats=3)
        self.assertGreater(imp[0], 1.0)
        self.assertEqual(imp[1], 0.0)

    def test_rejects_bad_input(self):
        X, y, predict = linear_setup()
        with self.assertRaises(ValueError):
            permutation_importance(predict, X, y, neg_mse, np.random.default_rng(0), repeats=0)
        with self.assertRaises(ValueError):
            permutation_importance(predict, X[:, 0], y, neg_mse, np.random.default_rng(0))
        with self.assertRaises(ValueError):
            permutation_importance(predict, X, y[:-1], neg_mse, np.random.default_rng(0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
