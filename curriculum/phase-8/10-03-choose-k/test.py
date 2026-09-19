import math
import time
import unittest

import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

from solution import choose_k, cv_accuracy

HX = np.array([[0.0], [0.1], [0.2], [5.0], [5.1], [5.2]])
HY = np.array([0, 0, 0, 1, 1, 1])


def brute_cv(X, y, k, folds):
    """Slow, literal version of the spec, used to check tie handling."""
    n = len(X)
    q, r = divmod(n, folds)
    sizes = [q + 1] * r + [q] * (folds - r)
    accs, start = [], 0
    for size in sizes:
        val = list(range(start, start + size))
        train = [i for i in range(n) if i not in val]
        correct = 0
        for v in val:
            ranked = sorted(range(len(train)), key=lambda p: (math.dist(X[v], X[train[p]]), p))[:k]
            votes, closest = {}, {}
            for p in ranked:
                label = int(y[train[p]])
                votes[label] = votes.get(label, 0) + 1
                closest.setdefault(label, math.dist(X[v], X[train[p]]))
            top = max(votes.values())
            pred = min((lab for lab in votes if votes[lab] == top), key=lambda lab: (closest[lab], lab))
            correct += pred == y[v]
        accs.append(correct / size)
        start += size
    return sum(accs) / folds


class TestChooseK(unittest.TestCase):
    def test_hand_example(self):
        self.assertAlmostEqual(cv_accuracy(HX, HY, 1, 3), 1.0, places=12)
        self.assertAlmostEqual(cv_accuracy(HX, HY, 2, 3), 1.0, places=12)
        self.assertAlmostEqual(cv_accuracy(HX, HY, 3, 3), 1 / 3, places=12)
        self.assertIsInstance(cv_accuracy(HX, HY, 1, 3), float)

    def test_ties_go_to_smaller_k(self):
        self.assertEqual(choose_k(HX, HY, [3, 2, 1], 3), 1)
        self.assertEqual(choose_k(HX, HY, [2, 3], 3), 2)
        rng = np.random.default_rng(0)
        X = np.vstack([rng.normal(-10, 1, size=(30, 2)), rng.normal(10, 1, size=(30, 2))])
        y = np.repeat([0, 1], 30)
        perm = rng.permutation(60)
        self.assertEqual(choose_k(X[perm], y[perm], [9, 5, 7, 3], 5), 3)

    def test_matches_sklearn_kfold_with_uneven_folds(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(203, 3))
        y = (X[:, 0] + X[:, 1] + 0.8 * rng.normal(size=203) > 0).astype(int)
        for k in [1, 5, 11]:
            expected = cross_val_score(KNeighborsClassifier(n_neighbors=k), X, y, cv=KFold(5)).mean()
            self.assertAlmostEqual(cv_accuracy(X, y, k, 5), expected, places=12)

    def test_noisy_labels_prefer_larger_k(self):
        rng = np.random.default_rng(2)
        X = rng.normal(size=(300, 2))
        y = (X[:, 0] > 0).astype(int)
        flip = rng.random(300) < 0.2
        y[flip] = 1 - y[flip]
        ks = [1, 3, 9, 15, 25]
        scores = {k: cross_val_score(KNeighborsClassifier(n_neighbors=k), X, y, cv=KFold(5)).mean() for k in ks}
        best = min(ks, key=lambda k: (-scores[k], k))
        self.assertNotEqual(best, 1)
        self.assertEqual(choose_k(X, y, ks, 5), best)

    def test_tie_rules_on_grid_data(self):
        rng = np.random.default_rng(3)
        X = rng.integers(0, 4, size=(40, 2)).astype(float)  # many equal distances
        y = rng.integers(0, 3, size=40)
        for k in [2, 4, 6]:
            for folds in [3, 7]:
                self.assertAlmostEqual(cv_accuracy(X, y, k, folds), brute_cv(X, y, k, folds), places=12)

    def test_fast_enough(self):
        rng = np.random.default_rng(4)
        X = rng.normal(size=(600, 5))
        y = (X[:, 0] > 0).astype(int)
        start = time.perf_counter()
        choose_k(X, y, [1, 3, 5, 7, 9, 11, 15, 21, 31, 51], 10)
        self.assertLess(time.perf_counter() - start, 3.0)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            choose_k(HX, HY, [5], 3)
        with self.assertRaises(ValueError):
            choose_k(HX, HY, [], 3)
        with self.assertRaises(ValueError):
            choose_k(HX, HY, [0], 3)
        with self.assertRaises(ValueError):
            cv_accuracy(HX, HY, 1, 1)
        with self.assertRaises(ValueError):
            cv_accuracy(HX, HY, 1, 7)
        # n = 7, folds = 3: sizes 3, 2, 2, so the smallest training set has 4 rows
        X7 = np.arange(7.0)[:, None]
        y7 = np.array([0, 1, 0, 1, 0, 1, 0])
        cv_accuracy(X7, y7, 4, 3)
        with self.assertRaises(ValueError):
            cv_accuracy(X7, y7, 5, 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
