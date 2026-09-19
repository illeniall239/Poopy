import random
import unittest

from sklearn.metrics import confusion_matrix

from solution import group_metrics

Y_TRUE = [1, 1, 0, 0, 1, 0, 0, 0]
Y_PRED = [1, 0, 0, 0, 1, 1, 1, 0]
GROUPS = ["a", "a", "a", "a", "b", "b", "b", "b"]


class TestGroupMetrics(unittest.TestCase):
    def assertMetrics(self, got, want):
        self.assertEqual(set(got), set(want))
        for key, value in want.items():
            if value is None:
                self.assertIsNone(got[key], key)
            else:
                self.assertAlmostEqual(got[key], value, places=9, msg=key)

    def test_hand_computed(self):
        m = group_metrics(Y_TRUE, Y_PRED, GROUPS)
        self.assertEqual(set(m), {"a", "b"})
        self.assertMetrics(m["a"], {"n": 4, "selection_rate": 0.25, "tpr": 0.5, "fpr": 0.0, "accuracy": 0.75})
        self.assertMetrics(m["b"], {"n": 4, "selection_rate": 0.75, "tpr": 1.0, "fpr": 2 / 3, "accuracy": 0.5})
        self.assertIsInstance(m["a"]["n"], int)

    def test_undefined_rates_are_none(self):
        m = group_metrics([0, 0, 1, 1], [1, 0, 1, 0], ["x", "x", "y", "y"])
        self.assertIsNone(m["x"]["tpr"])
        self.assertAlmostEqual(m["x"]["fpr"], 0.5)
        self.assertIsNone(m["y"]["fpr"])
        self.assertAlmostEqual(m["y"]["tpr"], 0.5)

    def test_equal_accuracy_different_error_types(self):
        # Group p only suffers false negatives, group q only false positives.
        y_true = [1, 1, 0, 0, 1, 1, 0, 0]
        y_pred = [0, 1, 0, 0, 1, 1, 1, 0]
        groups = ["p"] * 4 + ["q"] * 4
        m = group_metrics(y_true, y_pred, groups)
        self.assertAlmostEqual(m["p"]["accuracy"], m["q"]["accuracy"])
        self.assertAlmostEqual(m["p"]["tpr"], 0.5)
        self.assertAlmostEqual(m["q"]["tpr"], 1.0)
        self.assertAlmostEqual(m["p"]["fpr"], 0.0)
        self.assertAlmostEqual(m["q"]["fpr"], 0.5)

    def test_any_hashable_group_and_single_group(self):
        m = group_metrics([1, 0, 1], [1, 1, 1], [(1, "x"), (1, "x"), (1, "x")])
        self.assertMetrics(m[(1, "x")], {"n": 3, "selection_rate": 1.0, "tpr": 1.0, "fpr": 1.0, "accuracy": 2 / 3})

    def test_matches_sklearn_confusion_matrix(self):
        rng = random.Random(0)
        n = 3000
        y_true = [rng.randint(0, 1) for _ in range(n)]
        y_pred = [rng.randint(0, 1) for _ in range(n)]
        groups = [rng.choice(["g1", "g2", "g3", "g4"]) for _ in range(n)]
        m = group_metrics(y_true, y_pred, groups)
        for g in ["g1", "g2", "g3", "g4"]:
            idx = [j for j in range(n) if groups[j] == g]
            t = [y_true[j] for j in idx]
            p = [y_pred[j] for j in idx]
            tn, fp, fn, tp = confusion_matrix(t, p, labels=[0, 1]).ravel()
            self.assertMetrics(m[g], {
                "n": len(idx),
                "selection_rate": (tp + fp) / len(idx),
                "tpr": tp / (tp + fn),
                "fpr": fp / (fp + tn),
                "accuracy": (tp + tn) / len(idx),
            })

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            group_metrics([], [], [])
        with self.assertRaises(ValueError):
            group_metrics([1], [1, 0], ["x"])
        with self.assertRaises(ValueError):
            group_metrics([1, 0], [1, 0], ["x"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
