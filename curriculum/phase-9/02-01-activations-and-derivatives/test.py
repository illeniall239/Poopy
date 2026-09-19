import math
import unittest

from solution import (
    sigmoid, d_sigmoid, tanh, d_tanh, relu, d_relu,
    leaky_relu, d_leaky_relu, gelu, d_gelu,
)

POINTS = [-4.0, -2.5, -1.0, -0.3, 0.2, 0.7, 1.5, 3.0]
H = 1e-6


def numeric(f, x):
    return (f(x + H) - f(x - H)) / (2 * H)


class TestActivations(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(sigmoid(0.0), 0.5)
        self.assertAlmostEqual(sigmoid(2.0), 1 / (1 + math.exp(-2.0)))
        self.assertAlmostEqual(tanh(0.5), math.tanh(0.5))
        self.assertEqual(relu(-2.0), 0.0)
        self.assertEqual(relu(3.5), 3.5)
        self.assertAlmostEqual(leaky_relu(-2.0), -0.02)
        self.assertAlmostEqual(leaky_relu(-2.0, alpha=0.2), -0.4)
        self.assertAlmostEqual(leaky_relu(4.0), 4.0)
        self.assertAlmostEqual(gelu(1.0), 0.8413447460685429, places=12)
        self.assertAlmostEqual(gelu(-1.0), -0.15865525393145707, places=12)

    def test_sigmoid_does_not_overflow(self):
        self.assertAlmostEqual(sigmoid(-1000.0), 0.0, places=12)
        self.assertAlmostEqual(sigmoid(1000.0), 1.0, places=12)
        self.assertAlmostEqual(d_sigmoid(-1000.0), 0.0, places=12)
        self.assertAlmostEqual(d_sigmoid(1000.0), 0.0, places=12)

    def test_derivatives_at_zero(self):
        self.assertAlmostEqual(d_sigmoid(0.0), 0.25)
        self.assertAlmostEqual(d_tanh(0.0), 1.0)
        self.assertEqual(d_relu(0.0), 0.0)
        self.assertAlmostEqual(d_leaky_relu(0.0), 0.01)
        self.assertAlmostEqual(d_leaky_relu(0.0, 0.2), 0.2)
        self.assertAlmostEqual(d_gelu(0.0), 0.5)

    def test_smooth_derivatives_match_central_difference(self):
        for f, df in [(sigmoid, d_sigmoid), (tanh, d_tanh), (gelu, d_gelu)]:
            for x in POINTS:
                self.assertAlmostEqual(df(x), numeric(f, x), delta=1e-6, msg=f"{f.__name__} at {x}")

    def test_relu_family_derivatives_away_from_zero(self):
        leaky3 = lambda z: leaky_relu(z, 0.3)
        for x in POINTS:
            self.assertAlmostEqual(d_relu(x), numeric(relu, x), delta=1e-6, msg=f"relu at {x}")
            self.assertAlmostEqual(d_leaky_relu(x), numeric(leaky_relu, x), delta=1e-6, msg=f"leaky at {x}")
            self.assertAlmostEqual(d_leaky_relu(x, 0.3), numeric(leaky3, x), delta=1e-6, msg=f"leaky 0.3 at {x}")

    def test_saturation_kills_the_gradient(self):
        self.assertLess(d_sigmoid(20.0), 1e-8)
        self.assertLess(d_tanh(10.0), 1e-7)
        self.assertLessEqual(max(d_sigmoid(x / 10) for x in range(-50, 51)), 0.25 + 1e-12)

    def test_dead_relu_gets_no_gradient_but_leaky_does(self):
        for x in (-0.001, -1.0, -50.0):
            self.assertEqual(d_relu(x), 0.0)
            self.assertAlmostEqual(d_leaky_relu(x, 0.05), 0.05)


if __name__ == "__main__":
    unittest.main(verbosity=2)
