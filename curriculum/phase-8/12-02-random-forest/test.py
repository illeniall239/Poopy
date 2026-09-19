import random
import unittest

from solution import RandomForest


def noisy_data(seed, n, noise):
    # Two informative features (label = x0 + x1 > 0), two pure-noise features, and a share of flipped labels.
    rng = random.Random(seed)
    X = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(n)]
    y = []
    for r in X:
        label = int(r[0] + r[1] > 0)
        y.append(1 - label if rng.random() < noise else label)
    return X, y


def accuracy(pred, y):
    return sum(p == t for p, t in zip(pred, y)) / len(y)


def two_feature_data():
    # Feature 0 separates the classes perfectly; feature 1 only partly.
    rng = random.Random(5)
    X, y = [], []
    for i in range(60):
        label = i % 2
        X.append([label + rng.uniform(-0.4, 0.4), label + rng.uniform(-1.0, 1.0)])
        y.append(label)
    return X, y


class TestRandomForest(unittest.TestCase):
    def test_fit_returns_self_and_grows_n_trees(self):
        X, y = noisy_data(1, 60, 0.1)
        forest = RandomForest(n_trees=7, max_features=2, seed=0)
        self.assertIs(forest.fit(X, y), forest)
        self.assertEqual(len(forest.trees), 7)
        pred = forest.predict(X[:10])
        self.assertEqual(len(pred), 10)
        self.assertTrue(set(pred) <= {0, 1})

    def test_same_seed_same_forest(self):
        X, y = noisy_data(2, 80, 0.2)
        a = RandomForest(n_trees=5, max_features=2, seed=3).fit(X, y)
        b = RandomForest(n_trees=5, max_features=2, seed=3).fit(X, y)
        self.assertEqual(a.trees, b.trees)
        probe, _ = noisy_data(9, 50, 0.0)
        self.assertEqual(a.predict(probe), b.predict(probe))

    def test_beats_a_single_full_depth_tree_on_noisy_data(self):
        from sklearn.tree import DecisionTreeClassifier

        X_train, y_train = noisy_data(100, 150, 0.2)
        X_test, y_test = noisy_data(200, 400, 0.0)
        tree_acc = accuracy(DecisionTreeClassifier(random_state=0).fit(X_train, y_train).predict(X_test), y_test)
        forest_accs = [
            accuracy(RandomForest(n_trees=25, max_features=2, seed=s).fit(X_train, y_train).predict(X_test), y_test)
            for s in range(3)
        ]
        for acc in forest_accs:
            self.assertGreater(acc, tree_acc)
        self.assertGreater(sum(forest_accs) / 3, tree_acc + 0.05)

    def test_each_split_sees_a_random_feature_subset(self):
        X, y = two_feature_data()
        restricted = RandomForest(n_trees=20, max_features=1, seed=0).fit(X, y)
        self.assertEqual({tree["feature"] for tree in restricted.trees}, {0, 1})
        full = RandomForest(n_trees=20, max_features=2, seed=0).fit(X, y)
        self.assertEqual({tree["feature"] for tree in full.trees}, {0})

    def test_trees_see_different_bootstrap_samples(self):
        X, y = noisy_data(3, 60, 0.25)
        forest = RandomForest(n_trees=6, max_features=4, seed=1).fit(X, y)
        self.assertGreater(len({repr(tree) for tree in forest.trees}), 1)

    def test_max_depth_limits_every_tree(self):
        def depth(tree):
            return 0 if "value" in tree else 1 + max(depth(tree["left"]), depth(tree["right"]))

        X, y = noisy_data(4, 80, 0.2)
        forest = RandomForest(n_trees=5, max_features=2, max_depth=2, seed=0).fit(X, y)
        self.assertTrue(all(depth(tree) <= 2 for tree in forest.trees))
        self.assertTrue(all(depth(tree) >= 1 for tree in forest.trees))

    def test_string_labels(self):
        X = [[float(i), float(i % 3)] for i in range(30)]
        y = ["small" if i < 15 else "big" for i in range(30)]
        forest = RandomForest(n_trees=9, max_features=1, seed=2).fit(X, y)
        self.assertEqual(forest.predict([[0.0, 0.0], [29.0, 2.0]]), ["small", "big"])

    def test_rejects_bad_settings(self):
        X, y = noisy_data(5, 20, 0.0)
        with self.assertRaises(ValueError):
            RandomForest(n_trees=0, max_features=2).fit(X, y)
        with self.assertRaises(ValueError):
            RandomForest(n_trees=3, max_features=5).fit(X, y)
        with self.assertRaises(ValueError):
            RandomForest(n_trees=3, max_features=0).fit(X, y)
        with self.assertRaises(ValueError):
            RandomForest(n_trees=3, max_features=2).fit(X, y[:-1])
        with self.assertRaises(RuntimeError):
            RandomForest(n_trees=3, max_features=2).predict(X)


if __name__ == "__main__":
    unittest.main(verbosity=2)
