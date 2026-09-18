import math
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import gradient_check, numeric_jacobian


class TestJacobianAndGradcheck(unittest.TestCase):
    def test_jacobian_example(self):
        f = lambda v: [v[0] * v[1], v[0] + v[1], v[0] ** 2]  # noqa: E731
        J = numeric_jacobian(f, [2.0, 3.0])
        self.assertEqual(len(J), 3)
        self.assertEqual(len(J[0]), 2)
        assert_allclose(J, [[3.0, 2.0], [1.0, 1.0], [4.0, 0.0]], atol=1e-6)

    def test_jacobian_scalar_and_identity(self):
        assert_allclose(numeric_jacobian(lambda v: [v[0]], [1.5]), [[1.0]], atol=1e-9)
        assert_allclose(numeric_jacobian(lambda v: list(v), [1.0, 2.0, 3.0]), np.eye(3), atol=1e-9)

    def test_jacobian_of_linear_map_is_the_matrix(self):
        rng = np.random.default_rng(0)
        A = rng.normal(size=(4, 6))
        f = lambda v: (A @ np.asarray(v)).tolist()  # noqa: E731
        assert_allclose(numeric_jacobian(f, rng.normal(size=6).tolist()), A, atol=1e-6)

    def test_jacobian_softmax(self):
        def softmax(v):
            m = max(v)
            e = [math.exp(t - m) for t in v]
            s = sum(e)
            return [t / s for t in e]

        x = [0.2, -1.0, 0.7]
        p = softmax(x)
        expected = [[p[i] * ((i == j) - p[j]) for j in range(3)] for i in range(3)]
        assert_allclose(numeric_jacobian(softmax, x), expected, atol=1e-6)

    def test_jacobian_errors_and_call_count(self):
        with self.assertRaises(ValueError):
            numeric_jacobian(lambda v: [v[0]], [1.0], h=0.0)
        with self.assertRaises(ValueError):
            numeric_jacobian(lambda v: [0.0], [])
        calls = []
        numeric_jacobian(lambda v: (calls.append(1), [v[0] + v[1], v[0] * v[1]])[1], [1.0, 2.0])
        self.assertLessEqual(len(calls), 5)

    def test_gradient_check_pass_and_fail(self):
        self.assertLess(gradient_check([2.0, 4.0], [2.0000001, 4.0]), 1e-7)
        self.assertEqual(gradient_check([2.0, 4.0], [2.0, 4.0]), 0.0)
        self.assertGreater(gradient_check([2.0, 4.0], [2.0, 4.4]), 1e-3)
        self.assertAlmostEqual(gradient_check([2.0, 4.0], [2.0, 4.4]), 0.4 / (math.sqrt(20) + math.sqrt(4 + 4.4**2)))

    def test_gradient_check_relative_not_absolute(self):
        self.assertLess(gradient_check([1e6, 1e6], [1e6 + 1, 1e6]), 1e-6)
        small = gradient_check([1.0, 2.0], [1.0, 2.1])
        big = gradient_check([1e6, 2e6], [1e6, 2.1e6])
        self.assertAlmostEqual(small, big, places=12)

    def test_gradient_check_zeros_and_mismatch(self):
        self.assertEqual(gradient_check([0.0, 0.0], [0.0, 0.0]), 0.0)
        with self.assertRaises(ValueError):
            gradient_check([1.0], [1.0, 2.0])

    def test_wrong_analytic_gradient_is_caught(self):
        def loss(v):
            return [sum(t**2 for t in v)]

        x = [0.5, -1.5, 2.0]
        numeric = numeric_jacobian(loss, x)[0]
        correct = [2 * t for t in x]
        wrong = [t for t in x]  # forgot the factor 2
        self.assertLess(gradient_check(correct, numeric), 1e-6)
        self.assertGreater(gradient_check(wrong, numeric), 1e-2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
