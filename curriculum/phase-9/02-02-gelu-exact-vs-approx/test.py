import math
import unittest

import torch
import torch.nn.functional as F

from solution import gelu_exact, gelu_tanh

GRID = [i / 50 for i in range(-400, 401)]  # -8 .. 8


class TestGelu(unittest.TestCase):
    def test_exact_known_values(self):
        self.assertEqual(gelu_exact(0.0), 0.0)
        self.assertAlmostEqual(gelu_exact(1.0), 0.8413447460685429, places=12)
        self.assertAlmostEqual(gelu_exact(-1.0), -0.15865525393145707, places=12)
        self.assertAlmostEqual(gelu_exact(-3.0), -0.0040496940948904, places=12)

    def test_tanh_known_values(self):
        self.assertEqual(gelu_tanh(0.0), 0.0)
        self.assertAlmostEqual(gelu_tanh(1.0), 0.8411919906082768, places=12)
        self.assertAlmostEqual(gelu_tanh(-3.0), -0.0036373920817729943, places=12)

    def test_matches_pytorch_both_ways(self):
        x = torch.tensor(GRID[::20], dtype=torch.float64)
        exact = F.gelu(x).tolist()
        approx = F.gelu(x, approximate="tanh").tolist()
        for xi, e, a in zip(x.tolist(), exact, approx):
            self.assertAlmostEqual(gelu_exact(xi), e, places=12, msg=f"exact at {xi}")
            self.assertAlmostEqual(gelu_tanh(xi), a, places=12, msg=f"tanh at {xi}")

    def test_close_but_not_identical(self):
        gaps = [abs(gelu_exact(x) - gelu_tanh(x)) for x in GRID]
        self.assertLess(max(gaps), 5e-4)
        self.assertGreater(max(gaps), 1e-4)

    def test_huge_inputs_do_not_raise(self):
        for f in (gelu_exact, gelu_tanh):
            self.assertAlmostEqual(f(1e6), 1e6, delta=1e-6)
            self.assertAlmostEqual(f(-1e6), 0.0, delta=1e-6)
            self.assertAlmostEqual(f(30.0), 30.0, delta=1e-9)

    def test_negative_region_is_not_flat(self):
        # Unlike ReLU, GELU changes with x for moderately negative inputs.
        for f in (gelu_exact, gelu_tanh):
            self.assertLess(f(-0.5), 0.0)
            self.assertNotAlmostEqual(f(-0.5), f(-1.5), places=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
