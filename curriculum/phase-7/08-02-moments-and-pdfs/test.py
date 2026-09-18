import math
import unittest

import numpy as np

from solution import bernoulli_pmf, expectation, gaussian_pdf, mean, variance


class TestMomentsAndPdfs(unittest.TestCase):
    def test_mean_and_variance_small(self):
        self.assertAlmostEqual(mean([1, 2, 3, 4]), 2.5)
        self.assertAlmostEqual(variance([1, 2, 3, 4]), 1.25)
        self.assertAlmostEqual(variance([1, 2, 3, 4], ddof=1), 5 / 3)
        self.assertAlmostEqual(variance([7, 7, 7]), 0.0)

    def test_mean_variance_errors(self):
        with self.assertRaises(ValueError):
            mean([])
        with self.assertRaises(ValueError):
            variance([5], ddof=1)
        with self.assertRaises(ValueError):
            variance([], ddof=0)

    def test_matches_numpy_random(self):
        rng = np.random.default_rng(0)
        x = rng.normal(loc=3, scale=2, size=10_000)
        self.assertAlmostEqual(mean(x.tolist()), float(np.mean(x)), places=9)
        self.assertAlmostEqual(variance(x.tolist()), float(np.var(x)), places=9)
        self.assertAlmostEqual(variance(x.tolist(), ddof=1), float(np.var(x, ddof=1)), places=9)

    def test_expectation(self):
        self.assertAlmostEqual(expectation([1, 2, 6], [0.5, 0.25, 0.25]), 2.5)
        self.assertAlmostEqual(expectation([1, 2, 3, 4, 5, 6], [1 / 6] * 6), 3.5)
        self.assertAlmostEqual(expectation([0, 1], [0.7, 0.3]), 0.3)

    def test_expectation_errors(self):
        with self.assertRaises(ValueError):
            expectation([1, 2], [0.5])
        with self.assertRaises(ValueError):
            expectation([1, 2], [0.6, 0.6])
        with self.assertRaises(ValueError):
            expectation([1, 2], [1.5, -0.5])

    def test_gaussian_pdf(self):
        self.assertAlmostEqual(gaussian_pdf(0.0), 1 / math.sqrt(2 * math.pi))
        self.assertAlmostEqual(gaussian_pdf(0.0, sigma=0.1), 10 / math.sqrt(2 * math.pi))
        self.assertGreater(gaussian_pdf(0.0, sigma=0.1), 1.0)
        self.assertAlmostEqual(gaussian_pdf(2.0, mu=2.0, sigma=3.0), 1 / (3 * math.sqrt(2 * math.pi)))
        self.assertAlmostEqual(gaussian_pdf(1.0), gaussian_pdf(-1.0))
        with self.assertRaises(ValueError):
            gaussian_pdf(0.0, sigma=0.0)

    def test_gaussian_pdf_integrates_to_one(self):
        xs = np.linspace(-8, 8, 20_001)
        ys = [gaussian_pdf(float(x), mu=0.5, sigma=1.3) for x in xs]
        self.assertAlmostEqual(float(np.trapezoid(ys, xs)), 1.0, places=6)

    def test_bernoulli_pmf(self):
        self.assertAlmostEqual(bernoulli_pmf(1, 0.3), 0.3)
        self.assertAlmostEqual(bernoulli_pmf(0, 0.3), 0.7)
        self.assertAlmostEqual(bernoulli_pmf(2, 0.3), 0.0)
        self.assertAlmostEqual(bernoulli_pmf(-1, 0.3), 0.0)
        with self.assertRaises(ValueError):
            bernoulli_pmf(1, 1.2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
