import math
import unittest

from solution import forward_derivative, numeric_derivative


class TestNumericDerivative(unittest.TestCase):
    def test_polynomial(self):
        self.assertAlmostEqual(numeric_derivative(lambda x: x**2, 3.0), 6.0, places=8)
        self.assertAlmostEqual(numeric_derivative(lambda x: 5 * x + 1, -2.0), 5.0, places=8)

    def test_transcendental(self):
        self.assertAlmostEqual(numeric_derivative(math.sin, 0.0), 1.0, places=8)
        self.assertAlmostEqual(numeric_derivative(math.cos, 1.0), -math.sin(1.0), places=8)
        self.assertAlmostEqual(numeric_derivative(math.exp, 1.0), math.e, places=8)
        self.assertAlmostEqual(numeric_derivative(math.log, 2.0), 0.5, places=8)

    def test_forward_difference(self):
        self.assertAlmostEqual(forward_derivative(lambda x: 5 * x + 1, 0.0), 5.0, places=8)
        self.assertAlmostEqual(forward_derivative(lambda x: x**3, 2.0, h=1e-2), 12.0601, places=6)

    def test_invalid_h(self):
        with self.assertRaises(ValueError):
            numeric_derivative(math.exp, 0.0, h=0.0)
        with self.assertRaises(ValueError):
            forward_derivative(math.exp, 0.0, h=-1e-3)

    def test_central_error_is_second_order(self):
        f = lambda x: x**3  # noqa: E731
        errors = [abs(numeric_derivative(f, 2.0, h=h) - 12.0) for h in (1e-2, 1e-3, 1e-4, 1e-5)]
        self.assertAlmostEqual(errors[0], 1e-4, delta=1e-6)
        for a, b in zip(errors, errors[1:]):
            self.assertLess(b, a)
        self.assertAlmostEqual(errors[0] / errors[1], 100.0, delta=2.0)

    def test_forward_error_is_first_order(self):
        f = lambda x: x**3  # noqa: E731
        e1 = abs(forward_derivative(f, 2.0, h=1e-2) - 12.0)
        e2 = abs(forward_derivative(f, 2.0, h=1e-3) - 12.0)
        self.assertAlmostEqual(e1 / e2, 10.0, delta=0.2)
        self.assertLess(abs(numeric_derivative(f, 2.0, h=1e-2) - 12.0), e1)

    def test_exactly_two_evaluations(self):
        calls = []

        def f(x):
            calls.append(x)
            return x * x

        numeric_derivative(f, 1.0, h=0.5)
        self.assertEqual(sorted(calls), [0.5, 1.5])


if __name__ == "__main__":
    unittest.main(verbosity=2)
