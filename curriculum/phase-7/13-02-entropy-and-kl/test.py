import math
import unittest

import numpy as np

from solution import cross_entropy, entropy, kl


class TestEntropyAndKl(unittest.TestCase):
    def test_entropy_values(self):
        self.assertAlmostEqual(entropy([0.5, 0.5]), math.log(2), places=12)
        self.assertAlmostEqual(entropy([1.0, 0.0]), 0.0, places=12)
        self.assertAlmostEqual(entropy([0.25] * 4), math.log(4), places=12)
        self.assertAlmostEqual(entropy([1.0]), 0.0, places=12)

    def test_entropy_max_at_uniform(self):
        rng = np.random.default_rng(0)
        for n in [2, 5, 50]:
            p = rng.dirichlet(np.ones(n)).tolist()
            self.assertLessEqual(entropy(p), math.log(n) + 1e-12)

    def test_cross_entropy_values(self):
        self.assertAlmostEqual(cross_entropy([1.0, 0.0], [0.9, 0.1]), -math.log(0.9), places=12)
        self.assertAlmostEqual(cross_entropy([0.5, 0.5], [0.5, 0.5]), math.log(2), places=12)
        self.assertEqual(cross_entropy([1.0, 0.0], [0.0, 1.0]), math.inf)
        self.assertAlmostEqual(cross_entropy([0.0, 1.0], [0.0, 1.0]), 0.0, places=12)

    def test_kl_values_and_asymmetry(self):
        self.assertAlmostEqual(kl([0.5, 0.5], [0.5, 0.5]), 0.0, places=12)
        self.assertAlmostEqual(kl([0.5, 0.5], [0.9, 0.1]), 0.5 * math.log(0.5 / 0.9) + 0.5 * math.log(0.5 / 0.1), places=12)
        self.assertAlmostEqual(kl([0.9, 0.1], [0.5, 0.5]), 0.9 * math.log(1.8) + 0.1 * math.log(0.2), places=12)
        self.assertNotAlmostEqual(kl([0.5, 0.5], [0.9, 0.1]), kl([0.9, 0.1], [0.5, 0.5]), places=3)
        self.assertAlmostEqual(kl([1.0, 0.0], [0.5, 0.5]), math.log(2), places=12)
        self.assertEqual(kl([1.0, 0.0], [0.0, 1.0]), math.inf)

    def test_kl_nonnegative_and_zero_on_self(self):
        rng = np.random.default_rng(1)
        for n in [2, 7, 100]:
            p = rng.dirichlet(np.ones(n)).tolist()
            q = rng.dirichlet(np.ones(n)).tolist()
            self.assertGreaterEqual(kl(p, q), -1e-12)
            self.assertAlmostEqual(kl(p, p), 0.0, places=12)
            self.assertAlmostEqual(kl(p, q), cross_entropy(p, q) - entropy(p), places=12)

    def test_matches_numpy(self):
        rng = np.random.default_rng(2)
        p = rng.dirichlet(np.ones(1000))
        q = rng.dirichlet(np.ones(1000))
        self.assertAlmostEqual(entropy(p.tolist()), float(-(p * np.log(p)).sum()), places=10)
        self.assertAlmostEqual(cross_entropy(p.tolist(), q.tolist()), float(-(p * np.log(q)).sum()), places=10)
        self.assertAlmostEqual(kl(p.tolist(), q.tolist()), float((p * np.log(p / q)).sum()), places=10)

    def test_validation(self):
        for bad in [[], [0.6, 0.6], [1.5, -0.5], [0.3, 0.3]]:
            with self.assertRaises(ValueError):
                entropy(bad)
            with self.assertRaises(ValueError):
                cross_entropy([0.5, 0.5], bad)
            with self.assertRaises(ValueError):
                kl(bad, [0.5, 0.5])
        with self.assertRaises(ValueError):
            cross_entropy([0.5, 0.5], [1.0])
        with self.assertRaises(ValueError):
            kl([1.0], [0.5, 0.5])


if __name__ == "__main__":
    unittest.main(verbosity=2)
