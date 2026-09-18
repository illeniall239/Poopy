import math
import unittest

import numpy as np

from solution import relu, relu_prime, sigmoid, sigmoid_prime, tanh, tanh_prime


def central(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


POINTS = np.linspace(-6, 6, 200)


class TestActivationDerivatives(unittest.TestCase):
    def test_sigmoid_values(self):
        self.assertAlmostEqual(sigmoid(0.0), 0.5)
        self.assertAlmostEqual(sigmoid(2.0), 1 / (1 + math.exp(-2.0)))
        self.assertAlmostEqual(sigmoid(1000.0), 1.0)
        self.assertAlmostEqual(sigmoid(-1000.0), 0.0)
        self.assertGreaterEqual(sigmoid(-1000.0), 0.0)

    def test_sigmoid_prime_matches_numeric(self):
        self.assertAlmostEqual(sigmoid_prime(0.0), 0.25)
        for x in POINTS:
            self.assertAlmostEqual(sigmoid_prime(float(x)), central(sigmoid, float(x)), places=7)
            self.assertLessEqual(sigmoid_prime(float(x)), 0.25 + 1e-12)

    def test_tanh_values(self):
        self.assertAlmostEqual(tanh(0.0), 0.0)
        self.assertAlmostEqual(tanh(1.0), math.tanh(1.0))
        self.assertAlmostEqual(tanh(-30.0), -1.0)

    def test_tanh_prime_matches_numeric(self):
        self.assertAlmostEqual(tanh_prime(0.0), 1.0)
        for x in POINTS:
            self.assertAlmostEqual(tanh_prime(float(x)), central(tanh, float(x)), places=7)
            self.assertLessEqual(tanh_prime(float(x)), 1.0 + 1e-12)

    def test_relu_values(self):
        self.assertEqual(relu(-2.0), 0.0)
        self.assertEqual(relu(0.0), 0.0)
        self.assertEqual(relu(3.5), 3.5)

    def test_relu_prime_subgradient_convention(self):
        self.assertEqual(relu_prime(0.0), 0.0)
        self.assertEqual(relu_prime(3.0), 1.0)
        self.assertEqual(relu_prime(-1e-9), 0.0)
        for x in POINTS:
            if abs(x) > 1e-3:
                self.assertAlmostEqual(relu_prime(float(x)), central(relu, float(x)), places=7)

    def test_sigmoid_symmetry(self):
        for x in [0.3, 1.7, 4.2]:
            self.assertAlmostEqual(sigmoid(x) + sigmoid(-x), 1.0, places=12)
            self.assertAlmostEqual(sigmoid_prime(x), sigmoid_prime(-x), places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
