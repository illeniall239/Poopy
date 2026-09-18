import math
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import numeric_gradient


class TestNumericGradient(unittest.TestCase):
    def test_quadratic_bowl(self):
        assert_allclose(numeric_gradient(lambda p: p[0] ** 2 + p[1] ** 2, [1.0, 2.0]), [2.0, 4.0], atol=1e-6)

    def test_interacting_parameters(self):
        assert_allclose(numeric_gradient(lambda p: p[0] * p[1], [3.0, 5.0]), [5.0, 3.0], atol=1e-6)
        assert_allclose(
            numeric_gradient(lambda p: p[0] * p[1] * p[2], [2.0, 3.0, 4.0]), [12.0, 8.0, 6.0], atol=1e-6
        )

    def test_linear_and_constant(self):
        assert_allclose(numeric_gradient(lambda p: 3 * p[0] - p[1] + 7, [10.0, -1.0]), [3.0, -1.0], atol=1e-6)
        assert_allclose(numeric_gradient(lambda p: 5.0, [1.0, 2.0]), [0.0, 0.0], atol=1e-12)

    def test_zero_at_minimum(self):
        assert_allclose(numeric_gradient(lambda p: sum(x**2 for x in p), [0.0, 0.0, 0.0]), [0.0] * 3, atol=1e-9)

    def test_params_unchanged_and_length(self):
        params = [1.0, 2.0, 3.0]
        grad = numeric_gradient(lambda p: sum(p), params)
        self.assertEqual(params, [1.0, 2.0, 3.0])
        self.assertEqual(len(grad), 3)

    def test_invalid_h(self):
        with self.assertRaises(ValueError):
            numeric_gradient(lambda p: p[0], [1.0], h=0.0)

    def test_call_count_and_one_nudge_at_a_time(self):
        base = [1.0, 2.0, 3.0, 4.0]
        seen = []

        def f(p):
            seen.append(list(p))
            return sum(x**2 for x in p)

        numeric_gradient(f, base, h=0.01)
        self.assertEqual(len(seen), 8)
        for p in seen:
            changed = [i for i in range(4) if p[i] != base[i]]
            self.assertEqual(len(changed), 1)
            self.assertAlmostEqual(abs(p[changed[0]] - base[changed[0]]), 0.01)

    def test_matches_analytic_on_random_quadratic_form(self):
        rng = np.random.default_rng(0)
        n = 20
        A = rng.normal(size=(n, n))
        A = A @ A.T
        b = rng.normal(size=n)
        x = rng.normal(size=n)
        f = lambda p: float(0.5 * np.asarray(p) @ A @ np.asarray(p) - b @ np.asarray(p))  # noqa: E731
        assert_allclose(numeric_gradient(f, x.tolist()), A @ x - b, atol=1e-5)

    def test_transcendental(self):
        f = lambda p: math.exp(p[0]) * math.sin(p[1])  # noqa: E731
        x = [0.5, 1.2]
        expected = [math.exp(0.5) * math.sin(1.2), math.exp(0.5) * math.cos(1.2)]
        assert_allclose(numeric_gradient(f, x), expected, atol=1e-6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
