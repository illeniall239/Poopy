import random
import unittest

from sklearn.metrics import confusion_matrix as sk_confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score

from solution import confusion_matrix, macro_f1, precision_recall_f1


class TestConfusionAndPRF(unittest.TestCase):
    def test_binary_confusion_matrix(self):
        self.assertEqual(confusion_matrix([1, 0, 1, 1, 0], [1, 1, 0, 1, 0]), [[1, 1], [1, 2]])

    def test_confusion_matrix_with_explicit_labels(self):
        # a label that never occurs still gets its row and column, in the given order
        self.assertEqual(confusion_matrix([1, 1], [1, 0], labels=[1, 0, 2]), [[1, 1, 0], [0, 0, 0], [0, 0, 0]])
        with self.assertRaises(ValueError):
            confusion_matrix([1, 3], [1, 0], labels=[0, 1])

    def test_confusion_matrix_matches_sklearn(self):
        rng = random.Random(0)
        y_true = [rng.choice("abcd") for _ in range(500)]
        y_pred = [rng.choice("abce") for _ in range(500)]
        expected = sk_confusion_matrix(y_true, y_pred).tolist()
        self.assertEqual(confusion_matrix(y_true, y_pred), expected)

    def test_prf_hand_example(self):
        p, r, f = precision_recall_f1([1, 0, 1, 1, 0], [1, 1, 0, 1, 0])
        self.assertAlmostEqual(p, 2 / 3, places=12)
        self.assertAlmostEqual(r, 2 / 3, places=12)
        self.assertAlmostEqual(f, 2 / 3, places=12)

    def test_no_positive_predictions_is_zero_not_a_crash(self):
        self.assertEqual(precision_recall_f1([0] * 99 + [1], [0] * 100), (0.0, 0.0, 0.0))
        # no actual positives: recall is 0.0
        p, r, f = precision_recall_f1([0, 0, 0], [1, 0, 0])
        self.assertEqual((p, r, f), (0.0, 0.0, 0.0))

    def test_positive_class_matters(self):
        p, r, f = precision_recall_f1([1, 1, 0], [1, 0, 0], positive=0)
        self.assertAlmostEqual(p, 0.5, places=12)
        self.assertAlmostEqual(r, 1.0, places=12)
        self.assertAlmostEqual(f, 2 / 3, places=12)
        p, r, f = precision_recall_f1(["spam", "ham"], ["spam", "spam"], positive="spam")
        self.assertAlmostEqual(p, 0.5, places=12)
        self.assertAlmostEqual(r, 1.0, places=12)

    def test_prf_matches_sklearn(self):
        rng = random.Random(1)
        y_true = [1 if rng.random() < 0.2 else 0 for _ in range(1000)]
        y_pred = [1 if rng.random() < 0.3 else 0 for _ in range(1000)]
        p, r, f = precision_recall_f1(y_true, y_pred)
        self.assertAlmostEqual(p, precision_score(y_true, y_pred), places=12)
        self.assertAlmostEqual(r, recall_score(y_true, y_pred), places=12)
        self.assertAlmostEqual(f, f1_score(y_true, y_pred), places=12)

    def test_macro_f1(self):
        self.assertAlmostEqual(macro_f1(["a", "b", "c", "a"], ["a", "b", "b", "a"]), (1 + 2 / 3 + 0) / 3, places=12)
        rng = random.Random(2)
        y_true = [rng.choice([0, 1, 2, 3]) for _ in range(600)]
        y_pred = [rng.choice([0, 1, 2, 4]) for _ in range(600)]
        expected = f1_score(y_true, y_pred, average="macro", zero_division=0)
        self.assertAlmostEqual(macro_f1(y_true, y_pred), expected, places=12)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            confusion_matrix([1, 0], [1])
        with self.assertRaises(ValueError):
            precision_recall_f1([], [])
        with self.assertRaises(ValueError):
            macro_f1([1], [1, 0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
