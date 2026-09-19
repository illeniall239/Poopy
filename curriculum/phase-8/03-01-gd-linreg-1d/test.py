import random
import unittest

import numpy as np

from solution import gd_linreg_1d


def noisy_line(n, seed):
    rng = random.Random(seed)
    xs = [rng.uniform(-1, 1) for _ in range(n)]
    ys = [3.0 * x - 2.0 + rng.gauss(0, 0.3) for x in xs]
    return xs, ys


class TestGdLinreg1d(unittest.TestCase):
    def test_zero_epochs(self):
        w, b, hist = gd_linreg_1d([1, 2, 3], [2, 4, 6], 0.1, 0)
        self.assertEqual((w, b), (0.0, 0.0))
        self.assertEqual(len(hist), 1)
        self.assertAlmostEqual(hist[0], 56 / 3, places=10)

    def test_one_step_updates_w_and_b_simultaneously(self):
        # grad_w = 2/3 * (-2*1 - 4*2 - 6*3) = -56/3, grad_b = 2/3 * (-12) = -8.
        w, b, hist = gd_linreg_1d([1, 2, 3], [2, 4, 6], 0.1, 1)
        self.assertAlmostEqual(w, 5.6 / 3, places=10)
        self.assertAlmostEqual(b, 0.8, places=10)
        self.assertEqual(len(hist), 2)
        expected = sum((w * x + b - y) ** 2 for x, y in zip([1, 2, 3], [2, 4, 6])) / 3
        self.assertAlmostEqual(hist[1], expected, places=10)

    def test_converges_to_the_closed_form(self):
        xs, ys = noisy_line(200, seed=0)
        w, b, hist = gd_linreg_1d(xs, ys, 0.1, 3000)
        w_ls, b_ls = np.polyfit(xs, ys, 1)
        self.assertAlmostEqual(w, w_ls, places=6)
        self.assertAlmostEqual(b, b_ls, places=6)
        self.assertEqual(len(hist), 3001)
        closed_form_mse = sum((w_ls * x + b_ls - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
        self.assertAlmostEqual(hist[-1], closed_form_mse, places=9)

    def test_loss_never_increases_with_a_stable_rate(self):
        xs, ys = noisy_line(100, seed=1)
        _, _, hist = gd_linreg_1d(xs, ys, 0.2, 500)
        for before, after in zip(hist, hist[1:]):
            self.assertLessEqual(after, before + 1e-12)
        self.assertLess(hist[-1], hist[0] / 10)

    def test_too_large_a_rate_diverges(self):
        xs = [float(x) for x in range(10)]
        ys = [2.0 * x + 1.0 for x in xs]
        _, _, hist = gd_linreg_1d(xs, ys, 0.1, 20)
        self.assertEqual(len(hist), 21)
        self.assertGreater(hist[-1], hist[0] * 1000)
        for before, after in zip(hist[1:], hist[2:]):
            self.assertGreater(after, before)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            gd_linreg_1d([], [], 0.1, 10)
        with self.assertRaises(ValueError):
            gd_linreg_1d([1, 2], [1], 0.1, 10)
        with self.assertRaises(ValueError):
            gd_linreg_1d([1, 2], [1, 2], 0.0, 10)
        with self.assertRaises(ValueError):
            gd_linreg_1d([1, 2], [1, 2], 0.1, -1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
