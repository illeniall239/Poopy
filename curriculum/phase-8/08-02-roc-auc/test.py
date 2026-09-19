import random
import time
import unittest

from sklearn.metrics import roc_auc_score

from solution import auc_trapezoid, roc_auc, roc_curve


class TestRocAuc(unittest.TestCase):
    def test_hand_example(self):
        self.assertAlmostEqual(roc_auc([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]), 0.75, places=12)
        self.assertAlmostEqual(roc_auc([0, 1], [0.1, 0.9]), 1.0, places=12)
        self.assertAlmostEqual(roc_auc([1, 0], [0.1, 0.9]), 0.0, places=12)

    def test_ties_count_one_half(self):
        self.assertAlmostEqual(roc_auc([0, 1], [0.5, 0.5]), 0.5, places=12)
        self.assertAlmostEqual(roc_auc([1, 1, 0, 0], [0.3] * 4), 0.5, places=12)
        self.assertAlmostEqual(roc_auc([0, 0, 1, 1], [0.3] * 4), 0.5, places=12)
        # one positive tied with one of two negatives, above the other: (1 + 0.5) / 2
        self.assertAlmostEqual(roc_auc([1, 0, 0], [0.7, 0.7, 0.1]), 0.75, places=12)

    def test_matches_sklearn_with_many_ties(self):
        rng = random.Random(0)
        y = [rng.randint(0, 1) for _ in range(2000)]
        s = [round(rng.random() + 0.3 * yi, 1) for yi in y]  # rounding forces heavy ties
        self.assertAlmostEqual(roc_auc(y, s), roc_auc_score(y, s), places=12)

    def test_roc_curve_points(self):
        fpr, tpr = roc_curve([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8])
        self.assertEqual(fpr, [0.0, 0.0, 0.5, 0.5, 1.0])
        self.assertEqual(tpr, [0.0, 0.5, 0.5, 1.0, 1.0])
        # tied scores make one diagonal step
        fpr, tpr = roc_curve([1, 0, 1, 0], [0.5, 0.5, 0.5, 0.5])
        self.assertEqual(fpr, [0.0, 1.0])
        self.assertEqual(tpr, [0.0, 1.0])

    def test_trapezoid_matches_rank_formula(self):
        self.assertAlmostEqual(auc_trapezoid([0.0, 0.0, 0.5, 0.5, 1.0], [0.0, 0.5, 0.5, 1.0, 1.0]), 0.75, places=12)
        rng = random.Random(1)
        for _ in range(20):
            y = [rng.randint(0, 1) for _ in range(60)] + [0, 1]
            s = [rng.randint(0, 8) / 8 for _ in range(62)]
            self.assertAlmostEqual(auc_trapezoid(*roc_curve(y, s)), roc_auc(y, s), places=12)

    def test_random_scores_near_half_and_fast(self):
        rng = random.Random(2)
        y = [1 if rng.random() < 0.3 else 0 for _ in range(100_000)]
        s = [rng.random() for _ in y]
        start = time.perf_counter()
        auc = roc_auc(y, s)
        fpr, tpr = roc_curve(y, s)
        self.assertLess(time.perf_counter() - start, 3.0)
        self.assertAlmostEqual(auc, 0.5, delta=0.01)
        self.assertAlmostEqual(auc, roc_auc_score(y, s), places=10)
        self.assertEqual((fpr[-1], tpr[-1]), (1.0, 1.0))

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            roc_auc([1, 1], [0.2, 0.9])
        with self.assertRaises(ValueError):
            roc_auc([0, 0], [0.2, 0.9])
        with self.assertRaises(ValueError):
            roc_auc([0, 1], [0.2])
        with self.assertRaises(ValueError):
            roc_auc([0, 2], [0.2, 0.3])
        with self.assertRaises(ValueError):
            roc_curve([], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
