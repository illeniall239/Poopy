import random
import time
import unittest

from solution import best_threshold, pr_curve

Y = [1, 1, 0, 1, 0, 0]
S = [0.9, 0.8, 0.7, 0.6, 0.4, 0.2]


def brute_points(y, s):
    n_pos = sum(y)
    out = []
    for t in sorted(set(s), reverse=True):
        tp = sum(1 for yi, si in zip(y, s) if si >= t and yi == 1)
        fp = sum(1 for yi, si in zip(y, s) if si >= t and yi == 0)
        out.append((t, tp / (tp + fp), tp / n_pos))
    return out


class TestBestThreshold(unittest.TestCase):
    def assertPointsEqual(self, got, expected):
        self.assertEqual(len(got), len(expected))
        for (t, p, r), (et, ep, er) in zip(got, expected):
            self.assertEqual(t, et)
            self.assertAlmostEqual(p, ep, places=12)
            self.assertAlmostEqual(r, er, places=12)

    def test_pr_curve_hand_example(self):
        expected = [(0.9, 1.0, 1 / 3), (0.8, 1.0, 2 / 3), (0.7, 2 / 3, 2 / 3), (0.6, 0.75, 1.0), (0.4, 0.6, 1.0), (0.2, 0.5, 1.0)]
        self.assertPointsEqual(pr_curve(Y, S), expected)

    def test_pr_curve_groups_ties(self):
        self.assertPointsEqual(pr_curve([1, 0, 1, 0], [0.5, 0.5, 0.5, 0.1]), [(0.5, 2 / 3, 1.0), (0.1, 0.5, 1.0)])
        rng = random.Random(0)
        y = [rng.randint(0, 1) for _ in range(300)] + [1]
        s = [rng.randint(0, 20) / 20 for _ in range(301)]
        self.assertPointsEqual(pr_curve(y, s), brute_points(y, s))

    def test_best_f1(self):
        self.assertEqual(best_threshold(Y, S), 0.6)
        self.assertEqual(best_threshold(Y, S, "f1"), 0.6)
        self.assertEqual(best_threshold([1, 0, 0], [0.5, 0.5, 0.1]), 0.5)

    def test_precision_floor(self):
        self.assertEqual(best_threshold(Y, S, "precision_floor", min_precision=0.9), 0.8)
        self.assertEqual(best_threshold(Y, S, "precision_floor", min_precision=0.7), 0.6)
        self.assertEqual(best_threshold(Y, S, "precision_floor", min_precision=0.5), 0.6)

    def test_ties_go_to_the_higher_threshold(self):
        # F1 is 2/3 at both 0.9 and 0.3
        self.assertEqual(best_threshold([1, 0, 0, 1], [0.9, 0.7, 0.5, 0.3]), 0.9)
        # recall 1.0 at thresholds 0.6 and 0.4, both with precision >= 0.5
        self.assertEqual(best_threshold([1, 1, 0, 0], [0.8, 0.6, 0.4, 0.1], "precision_floor", min_precision=0.5), 0.6)

    def test_matches_brute_force_and_is_fast(self):
        rng = random.Random(1)
        y = [1 if rng.random() < 0.1 else 0 for _ in range(100_000)]
        s = [round(rng.random() + 0.4 * yi, 3) for yi in y]
        start = time.perf_counter()
        points = pr_curve(y, s)
        best = best_threshold(y, s)
        floor = best_threshold(y, s, "precision_floor", min_precision=0.8)
        self.assertLess(time.perf_counter() - start, 3.0)
        f1s = [(t, 2 * p * r / (p + r)) for t, p, r in points]
        top = max(f for _, f in f1s)
        self.assertEqual(best, max(t for t, f in f1s if f == top))
        ok = [(t, r) for t, p, r in points if p >= 0.8]
        top_r = max(r for _, r in ok)
        self.assertEqual(floor, max(t for t, r in ok if r == top_r))

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            best_threshold(Y, S, "precision_floor")
        with self.assertRaises(ValueError):
            best_threshold(Y, S, "precision_floor", min_precision=1.5)
        with self.assertRaises(ValueError):
            best_threshold([1, 0, 0], [0.1, 0.5, 0.9], "precision_floor", min_precision=0.9)
        with self.assertRaises(ValueError):
            best_threshold(Y, S, "accuracy")
        with self.assertRaises(ValueError):
            pr_curve([0, 0], [0.1, 0.2])
        with self.assertRaises(ValueError):
            pr_curve([1, 0], [0.1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
