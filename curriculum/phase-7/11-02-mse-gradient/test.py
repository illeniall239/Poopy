import unittest

import numpy as np

from solution import mse, mse_gradient

XS, YS = [1.0, 2.0, 3.0], [2.0, 4.0, 6.0]


def numeric_gradient(w, b, xs, ys, h=1e-5):
    dw = (mse(w + h, b, xs, ys) - mse(w - h, b, xs, ys)) / (2 * h)
    db = (mse(w, b + h, xs, ys) - mse(w, b - h, xs, ys)) / (2 * h)
    return dw, db


class TestMseGradient(unittest.TestCase):
    def test_loss_values(self):
        self.assertAlmostEqual(mse(2.0, 0.0, XS, YS), 0.0)
        self.assertAlmostEqual(mse(0.0, 0.0, XS, YS), 56 / 3)
        self.assertAlmostEqual(mse(1.0, 1.0, XS, YS), 5 / 3)

    def test_gradient_at_minimum_is_zero(self):
        dw, db = mse_gradient(2.0, 0.0, XS, YS)
        self.assertAlmostEqual(dw, 0.0)
        self.assertAlmostEqual(db, 0.0)

    def test_gradient_by_hand(self):
        dw, db = mse_gradient(0.0, 0.0, XS, YS)
        self.assertAlmostEqual(dw, -56 / 3)
        self.assertAlmostEqual(db, -8.0)
        dw, db = mse_gradient(1.0, 1.0, XS, YS)
        self.assertAlmostEqual(dw, -16 / 3)
        self.assertAlmostEqual(db, -2.0)

    def test_errors(self):
        with self.assertRaises(ValueError):
            mse(1.0, 0.0, [1.0, 2.0], [1.0])
        with self.assertRaises(ValueError):
            mse_gradient(1.0, 0.0, [], [])

    def test_step_against_gradient_lowers_loss(self):
        w, b = 0.0, 0.0
        before = mse(w, b, XS, YS)
        dw, db = mse_gradient(w, b, XS, YS)
        after = mse(w - 0.01 * dw, b - 0.01 * db, XS, YS)
        self.assertLess(after, before)

    def test_matches_numeric_on_random_data(self):
        rng = np.random.default_rng(0)
        for _ in range(5):
            n = int(rng.integers(5, 200))
            xs = rng.normal(size=n).tolist()
            ys = (3 * np.asarray(xs) - 1 + rng.normal(scale=0.5, size=n)).tolist()
            w, b = float(rng.normal()), float(rng.normal())
            analytic = mse_gradient(w, b, xs, ys)
            numeric = numeric_gradient(w, b, xs, ys)
            self.assertAlmostEqual(analytic[0], numeric[0], places=6)
            self.assertAlmostEqual(analytic[1], numeric[1], places=6)

    def test_matches_numpy_closed_form(self):
        rng = np.random.default_rng(1)
        xs = rng.uniform(-2, 2, size=1000)
        ys = rng.uniform(-2, 2, size=1000)
        w, b = 0.7, -0.3
        r = w * xs + b - ys
        dw, db = mse_gradient(w, b, xs.tolist(), ys.tolist())
        self.assertAlmostEqual(dw, float(2 * np.mean(r * xs)), places=9)
        self.assertAlmostEqual(db, float(2 * np.mean(r)), places=9)
        self.assertAlmostEqual(mse(w, b, xs.tolist(), ys.tolist()), float(np.mean(r**2)), places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
