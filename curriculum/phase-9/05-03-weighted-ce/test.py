import math
import unittest

import numpy as np
import torch
import torch.nn.functional as F

from solution import weighted_ce

STRICT = dict(over="raise", divide="raise", invalid="raise")


def torch_ce(logits, target, weights, reduction):
    w = None if weights is None else torch.tensor(weights, dtype=torch.float64)
    return F.cross_entropy(torch.tensor(logits, dtype=torch.float64), torch.tensor(target), weight=w, reduction=reduction).item()


class TestWeightedCE(unittest.TestCase):
    def test_log_two(self):
        got = weighted_ce([[0.0, 0.0]], [0])
        self.assertIsInstance(got, float)
        self.assertAlmostEqual(got, math.log(2), places=12)

    def test_mean_and_sum_unweighted(self):
        z, t = [[2.0, 0.0, -1.0], [0.5, 0.5, 3.0]], [0, 2]
        mean = weighted_ce(z, t)
        self.assertAlmostEqual(mean, torch_ce(z, t, None, "mean"), places=12)
        self.assertAlmostEqual(weighted_ce(z, t, reduction="sum"), 2 * mean, places=12)

    def test_weighted_mean_divides_by_target_weights(self):
        z = [[0.0, 0.0], [0.0, 0.0]]
        self.assertAlmostEqual(weighted_ce(z, [0, 1], [1.0, 3.0]), math.log(2), places=12)
        self.assertAlmostEqual(weighted_ce(z, [0, 1], [1.0, 3.0], "sum"), 4 * math.log(2), places=12)
        self.assertAlmostEqual(weighted_ce(z, [1, 1], [1.0, 3.0]), math.log(2), places=12)
        self.assertAlmostEqual(weighted_ce(z, [1, 1], [1.0, 3.0], "sum"), 6 * math.log(2), places=12)

    def test_matches_pytorch_random(self):
        torch.manual_seed(0)
        for n, c in [(8, 3), (32, 5), (1, 4)]:
            z = (torch.randn(n, c, dtype=torch.float64) * 4).numpy()
            t = torch.randint(0, c, (n,)).numpy()
            w = torch.rand(c, dtype=torch.float64).numpy() + 0.1
            for weights in (None, w):
                for red in ("mean", "sum"):
                    want = torch_ce(z, t, None if weights is None else weights.tolist(), red)
                    got = weighted_ce(z, t, weights, red)
                    self.assertAlmostEqual(got, want, delta=1e-9, msg=f"{n}x{c} {red} weighted={weights is not None}")

    def test_extreme_logits_are_stable(self):
        with np.errstate(**STRICT):
            self.assertAlmostEqual(weighted_ce(np.array([[1000.0, -1000.0]]), np.array([1])), 2000.0, places=9)
            self.assertAlmostEqual(weighted_ce(np.array([[1000.0, -1000.0]]), np.array([0])), 0.0, places=9)
            got = weighted_ce(np.array([[-1000.0, -1000.0, -1000.0]]), np.array([2]))
        self.assertAlmostEqual(got, math.log(3), places=9)

    def test_zero_weight_class_is_ignored_in_the_mean(self):
        z = [[3.0, 0.0], [0.0, 3.0], [1.0, 1.0]]
        t = [0, 0, 1]
        got = weighted_ce(z, t, [1.0, 0.0])
        self.assertAlmostEqual(got, torch_ce(z, t, [1.0, 0.0], "mean"), places=12)

    def test_bad_input(self):
        z = [[0.0, 1.0], [1.0, 0.0]]
        bad = [
            (([0.0, 1.0], [0]), {}),
            ((np.zeros((0, 3)), []), {}),
            ((z, [0]), {}),
            ((z, [0, 2]), {}),
            ((z, [0, -1]), {}),
            ((z, [0, 1], [1.0]), {}),
            ((z, [0, 1], [1.0, -1.0]), {}),
            ((z, [0, 1]), {"reduction": "none"}),
            ((z, [0, 0], [0.0, 1.0]), {"reduction": "mean"}),
        ]
        for args, kwargs in bad:
            with self.assertRaises(ValueError, msg=repr((args, kwargs))):
                weighted_ce(*args, **kwargs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
