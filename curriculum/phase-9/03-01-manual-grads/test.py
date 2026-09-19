import random
import unittest

from solution import manual_grads


def L(a, b, c, f):
    return (a * b + c) * f


def numeric(a, b, c, f, h=1e-6):
    args = {"a": a, "b": b, "c": c, "f": f}
    out = {}
    for k in args:
        up, down = dict(args), dict(args)
        up[k] += h
        down[k] -= h
        out[k] = (L(**up) - L(**down)) / (2 * h)
    return out


class TestManualGrads(unittest.TestCase):
    def assertGrads(self, got, want, tol=1e-9):
        self.assertEqual(set(got), {"a", "b", "c", "f"})
        for k in want:
            self.assertAlmostEqual(got[k], want[k], delta=tol, msg=f"dL/d{k}")

    def test_karpathy_example(self):
        self.assertGrads(manual_grads(2.0, -3.0, 10.0, -2.0), {"a": 6.0, "b": -4.0, "c": -2.0, "f": 4.0})

    def test_all_ones(self):
        self.assertGrads(manual_grads(1.0, 1.0, 1.0, 1.0), {"a": 1.0, "b": 1.0, "c": 1.0, "f": 2.0})

    def test_zeros(self):
        self.assertGrads(manual_grads(0.0, 0.0, 0.0, 0.0), {"a": 0.0, "b": 0.0, "c": 0.0, "f": 0.0})

    def test_chain_multiplies_not_adds(self):
        # adding along the chain would give dL/da = b + f = 7, not b * f = 12
        self.assertGrads(manual_grads(5.0, 3.0, -1.0, 4.0), {"a": 12.0, "b": 20.0, "c": 4.0, "f": 14.0})

    def test_matches_numeric_on_random_inputs(self):
        rng = random.Random(0)
        for _ in range(20):
            a, b, c, f = (rng.uniform(-10, 10) for _ in range(4))
            self.assertGrads(manual_grads(a, b, c, f), numeric(a, b, c, f), tol=1e-6)

    def test_values_are_floats(self):
        for v in manual_grads(1.5, 2.0, 0.5, -1.0).values():
            self.assertIsInstance(v, float)


if __name__ == "__main__":
    unittest.main(verbosity=2)
