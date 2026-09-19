import random
import unittest
from collections import Counter

from solution import accuracy, majority_baseline_accuracy, majority_class, random_baseline_accuracy


def imbalanced(n, positive_rate, seed):
    rng = random.Random(seed)
    return [1 if rng.random() < positive_rate else 0 for _ in range(n)]


class TestBaselineClassifier(unittest.TestCase):
    def test_accuracy(self):
        self.assertAlmostEqual(accuracy(["a", "b", "a"], ["a", "a", "a"]), 2 / 3)
        self.assertAlmostEqual(accuracy([1, 0], [1, 0]), 1.0)
        self.assertAlmostEqual(accuracy([1, 0], [0, 1]), 0.0)

    def test_accuracy_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            accuracy([], [])
        with self.assertRaises(ValueError):
            accuracy([1, 0], [1])

    def test_majority_class_and_tie_rule(self):
        self.assertEqual(majority_class(["cat", "dog", "dog"]), "dog")
        self.assertEqual(majority_class([1, 0, 0, 1]), 1)
        self.assertEqual(majority_class(["b", "a", "a", "b", "c"]), "b")
        with self.assertRaises(ValueError):
            majority_class([])

    def test_majority_baseline_uses_train_labels_only(self):
        # In the second case the train majority is 0 but the val majority is 1; using it would score 0.75.
        self.assertAlmostEqual(majority_baseline_accuracy([0, 0, 0, 1], [0, 1, 0, 0]), 0.75)
        self.assertAlmostEqual(majority_baseline_accuracy([0, 0, 1], [1, 1, 1, 0]), 0.25)

    def test_majority_on_imbalanced_data_looks_impressive(self):
        train = imbalanced(5000, 0.08, seed=1)
        val = imbalanced(5000, 0.08, seed=2)
        self.assertGreater(majority_baseline_accuracy(train, val), 0.9)

    def test_random_baseline_matches_the_specified_draws(self):
        train = ["a", "b", "b", "c", "b"]
        val = ["b", "a", "c", "b", "b", "b", "a", "c"]
        preds = random.Random(3).choices(["a", "b", "c"], weights=[1, 3, 1], k=len(val))
        expected = sum(t == p for t, p in zip(val, preds)) / len(val)
        self.assertAlmostEqual(random_baseline_accuracy(train, val, 3), expected)

    def test_random_baseline_is_deterministic_and_uses_train_frequencies(self):
        train = imbalanced(20000, 0.1, seed=4)
        val = imbalanced(20000, 0.1, seed=5)
        a = random_baseline_accuracy(train, val, 7)
        self.assertEqual(a, random_baseline_accuracy(train, val, 7))
        # Frequency-weighted guessing: about 0.9^2 + 0.1^2 = 0.82; uniform guessing would give 0.5.
        p = Counter(train)[1] / len(train)
        q = Counter(val)[1] / len(val)
        self.assertAlmostEqual(a, p * q + (1 - p) * (1 - q), delta=0.01)
        self.assertLess(a, majority_baseline_accuracy(train, val))

    def test_random_baseline_rejects_empty_train(self):
        with self.assertRaises(ValueError):
            random_baseline_accuracy([], [1, 0], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
