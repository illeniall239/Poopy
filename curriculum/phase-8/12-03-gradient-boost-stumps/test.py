import math
import random
import unittest

from solution import gradient_boost_stumps, predict_boosted


def wavy(seed, n=40):
    # xs on a 0.25 grid so sklearn's float32 thresholds are exact.
    rng = random.Random(seed)
    xs = [0.25 * i for i in range(n)]
    rng.shuffle(xs)
    ys = [math.sin(x) * 3 + 0.5 * rng.gauss(0, 1) for x in xs]
    return xs, ys


class TestGradientBoostStumps(unittest.TestCase):
    def test_step_function_in_one_round(self):
        m = gradient_boost_stumps([1.0, 2.0, 3.0, 4.0], [0.0, 0.0, 10.0, 10.0], 1, 1.0)
        self.assertAlmostEqual(m["base"], 5.0)
        self.assertEqual(len(m["stumps"]), 1)
        t, left, right = m["stumps"][0]
        self.assertAlmostEqual(t, 2.5)
        self.assertAlmostEqual(left, -5.0)
        self.assertAlmostEqual(right, 5.0)
        self.assertEqual(len(m["losses"]), 2)
        self.assertAlmostEqual(m["losses"][0], 25.0)
        self.assertAlmostEqual(m["losses"][1], 0.0)
        self.assertAlmostEqual(predict_boosted(m, 1.0), 0.0)

    def test_learning_rate_shrinks_each_step(self):
        m = gradient_boost_stumps([1.0, 2.0, 3.0, 4.0], [0.0, 0.0, 10.0, 10.0], 1, 0.1)
        self.assertAlmostEqual(predict_boosted(m, 1.0), 4.5)
        self.assertAlmostEqual(predict_boosted(m, 4.0), 5.5)
        m2 = gradient_boost_stumps([1.0, 2.0, 3.0, 4.0], [0.0, 0.0, 10.0, 10.0], 2, 0.1)
        # round 2 fits the residuals left by round 1: 90% of the gap remains, so 4.5 -> 4.05
        self.assertAlmostEqual(predict_boosted(m2, 1.0), 4.05)

    def test_zero_rounds_is_the_mean(self):
        m = gradient_boost_stumps([0.0, 1.0, 2.0], [1.0, 2.0, 6.0], 0, 0.5)
        self.assertEqual(m["stumps"], [])
        self.assertEqual(len(m["losses"]), 1)
        self.assertAlmostEqual(predict_boosted(m, 10.0), 3.0)
        self.assertAlmostEqual(m["losses"][0], 14 / 3)

    def test_training_loss_decreases_every_round(self):
        xs, ys = wavy(1)
        for lr in (0.1, 0.5, 1.0):
            losses = gradient_boost_stumps(xs, ys, 30, lr)["losses"]
            self.assertEqual(len(losses), 31)
            for before, after in zip(losses, losses[1:]):
                self.assertLess(after, before)

    def test_losses_match_the_predictions(self):
        xs, ys = wavy(2)
        m = gradient_boost_stumps(xs, ys, 15, 0.3)
        mse = sum((y - predict_boosted(m, x)) ** 2 for x, y in zip(xs, ys)) / len(xs)
        self.assertAlmostEqual(m["losses"][-1], mse, places=8)

    def test_matches_sklearn_gradient_boosting(self):
        from sklearn.ensemble import GradientBoostingRegressor

        xs, ys = wavy(3)
        for n_rounds, lr in ((1, 1.0), (20, 0.3), (60, 0.1)):
            ours = gradient_boost_stumps(xs, ys, n_rounds, lr)
            theirs = GradientBoostingRegressor(
                n_estimators=n_rounds, learning_rate=lr, max_depth=1, criterion="squared_error"
            ).fit([[x] for x in xs], ys)
            probe = [0.25 * i + 0.1 for i in range(-4, 44)]
            expected = theirs.predict([[x] for x in probe])
            for x, e in zip(probe, expected):
                self.assertAlmostEqual(predict_boosted(ours, x), float(e), places=8)

    def test_no_extrapolation(self):
        xs = [float(x) for x in range(10)]
        ys = [2.0 * x for x in xs]
        m = gradient_boost_stumps(xs, ys, 50, 0.5)
        self.assertAlmostEqual(predict_boosted(m, 100.0), predict_boosted(m, 9.0))
        self.assertLess(predict_boosted(m, 100.0), 18.5)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            gradient_boost_stumps([], [], 3, 0.1)
        with self.assertRaises(ValueError):
            gradient_boost_stumps([1.0, 2.0], [1.0], 3, 0.1)
        with self.assertRaises(ValueError):
            gradient_boost_stumps([1.0, 1.0], [1.0, 2.0], 3, 0.1)
        with self.assertRaises(ValueError):
            gradient_boost_stumps([1.0, 2.0], [1.0, 2.0], -1, 0.1)
        with self.assertRaises(ValueError):
            gradient_boost_stumps([1.0, 2.0], [1.0, 2.0], 3, 0.0)
        with self.assertRaises(ValueError):
            gradient_boost_stumps([1.0, 2.0], [1.0, 2.0], 3, 1.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
