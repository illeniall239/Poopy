import math
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import stable_sigmoid, stable_sigmoid_np


def textbook(z):
    return 1.0 / (1.0 + math.exp(-z))


class TestStableSigmoid(unittest.TestCase):
    def test_moderate_values_match_textbook(self):
        for z in [0.0, 0.5, -0.5, 2.0, -2.0, 10.0, -10.0, 35.0, -35.0]:
            self.assertAlmostEqual(stable_sigmoid(z), textbook(z), delta=1e-12 * textbook(z))

    def test_returns_python_float(self):
        self.assertIsInstance(stable_sigmoid(1.5), float)
        self.assertIsInstance(stable_sigmoid(-1.5), float)

    def test_extremes_do_not_overflow(self):
        self.assertEqual(stable_sigmoid(1000.0), 1.0)
        self.assertEqual(stable_sigmoid(-1000.0), 0.0)
        self.assertEqual(stable_sigmoid(1e308), 1.0)
        self.assertEqual(stable_sigmoid(-1e308), 0.0)

    def test_small_tail_keeps_precision(self):
        for z in [-30.0, -40.0, -700.0]:
            expected = math.exp(z) / (1.0 + math.exp(z))
            self.assertGreater(stable_sigmoid(z), 0.0)
            self.assertLess(abs(stable_sigmoid(z) - expected), 1e-12 * expected)

    def test_symmetry(self):
        for z in [0.1, 1.0, 3.0, 7.5]:
            self.assertAlmostEqual(stable_sigmoid(-z), 1.0 - stable_sigmoid(z), places=12)

    def test_numpy_matches_scalar(self):
        z = np.linspace(-50, 50, 1001)
        expected = np.array([stable_sigmoid(float(v)) for v in z])
        assert_allclose(stable_sigmoid_np(z), expected, rtol=1e-12, atol=0)

    def test_numpy_no_warnings_at_extremes(self):
        z = np.array([-1000.0, -800.0, 0.0, 800.0, 1000.0])
        with np.errstate(over="raise", divide="raise", invalid="raise"):
            out = stable_sigmoid_np(z)
        assert_allclose(out, [0.0, 0.0, 0.5, 1.0, 1.0], atol=0)

    def test_numpy_keeps_shape(self):
        z = np.arange(-6.0, 6.0).reshape(3, 4)
        out = stable_sigmoid_np(z)
        self.assertEqual(out.shape, (3, 4))
        self.assertTrue(np.issubdtype(out.dtype, np.floating))
        with np.errstate(over="raise", divide="raise", invalid="raise"):
            out = stable_sigmoid_np(np.array([-745.0, -30.0]))
        assert_allclose(out[1], math.exp(-30) / (1 + math.exp(-30)), rtol=1e-12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
