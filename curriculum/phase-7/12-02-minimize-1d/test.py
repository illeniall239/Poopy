import unittest

from solution import minimize_1d

QUAD = lambda x: (x - 3) ** 2  # noqa: E731
DOUBLE_WELL = lambda x: x**4 - 3 * x**2 + x  # noqa: E731


class TestMinimize1D(unittest.TestCase):
    def test_quadratic_converges(self):
        x, steps = minimize_1d(QUAD, x0=0.0, lr=0.1)
        self.assertAlmostEqual(x, 3.0, places=6)
        self.assertGreater(steps, 5)
        self.assertLess(steps, 200)

    def test_already_at_minimum_takes_zero_steps(self):
        self.assertEqual(minimize_1d(QUAD, x0=3.0, lr=0.1), (3.0, 0))

    def test_max_steps_budget(self):
        x, steps = minimize_1d(QUAD, x0=0.0, lr=0.1, max_steps=5)
        self.assertEqual(steps, 5)
        self.assertAlmostEqual(x, 3.0 * (1 - 0.8**5), places=6)
        self.assertEqual(minimize_1d(QUAD, x0=0.0, lr=0.1, max_steps=0), (0.0, 0))

    def test_tighter_tolerance_never_fewer_steps(self):
        _, loose = minimize_1d(QUAD, x0=0.0, lr=0.1, tol=1e-3)
        _, tight = minimize_1d(QUAD, x0=0.0, lr=0.1, tol=1e-8)
        self.assertGreaterEqual(tight, loose)
        self.assertGreater(tight, loose)

    def test_two_basins(self):
        right, _ = minimize_1d(DOUBLE_WELL, x0=2.0, lr=0.02)
        left, _ = minimize_1d(DOUBLE_WELL, x0=-2.0, lr=0.02)
        self.assertAlmostEqual(right, 1.1309, places=3)
        self.assertAlmostEqual(left, -1.3008, places=3)
        self.assertLess(DOUBLE_WELL(left), DOUBLE_WELL(right))

    def test_divergence_raises(self):
        with self.assertRaises(RuntimeError):
            minimize_1d(lambda x: x**2, x0=1.0, lr=1.5)

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            minimize_1d(QUAD, 0.0, lr=0.0)
        with self.assertRaises(ValueError):
            minimize_1d(QUAD, 0.0, lr=0.1, tol=0.0)
        with self.assertRaises(ValueError):
            minimize_1d(QUAD, 0.0, lr=0.1, max_steps=-1)

    def test_scaled_curvature_changes_safe_lr(self):
        x, _ = minimize_1d(lambda x: 0.1 * x**2, x0=1.0, lr=1.5)
        self.assertAlmostEqual(x, 0.0, places=6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
