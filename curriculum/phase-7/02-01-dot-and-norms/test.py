import unittest

import numpy as np

from solution import cosine_similarity, dot, norm


class TestDotAndNorms(unittest.TestCase):
    def test_dot_basic(self):
        self.assertAlmostEqual(dot([1, 2, 3], [4, 5, 6]), 32.0)
        self.assertAlmostEqual(dot([1, 0], [0, 1]), 0.0)
        self.assertAlmostEqual(dot([1.5], [-2.0]), -3.0)

    def test_dot_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            dot([1, 2], [1])

    def test_norms(self):
        self.assertAlmostEqual(norm([3, 4]), 5.0)
        self.assertAlmostEqual(norm([3, 4], p=2), 5.0)
        self.assertAlmostEqual(norm([3, -4], p=1), 7.0)
        self.assertAlmostEqual(norm([0, 0, 0]), 0.0)
        self.assertAlmostEqual(norm([-2], p=1), 2.0)

    def test_norm_rejects_other_p(self):
        with self.assertRaises(ValueError):
            norm([1, 2], p=3)

    def test_cosine_basic(self):
        self.assertAlmostEqual(cosine_similarity([1, 1], [2, 2]), 1.0)
        self.assertAlmostEqual(cosine_similarity([1, 0], [0, 1]), 0.0)
        self.assertAlmostEqual(cosine_similarity([1, 0], [-1, 0]), -1.0)

    def test_cosine_rejects_zero_vector_and_mismatch(self):
        with self.assertRaises(ValueError):
            cosine_similarity([0, 0], [1, 2])
        with self.assertRaises(ValueError):
            cosine_similarity([1, 2], [0, 0])
        with self.assertRaises(ValueError):
            cosine_similarity([1, 2, 3], [1, 2])

    def test_matches_numpy_on_random_vectors(self):
        rng = np.random.default_rng(0)
        for _ in range(5):
            a = rng.normal(size=50)
            b = rng.normal(size=50)
            self.assertAlmostEqual(dot(list(a), list(b)), float(a @ b), places=9)
            self.assertAlmostEqual(norm(list(a)), float(np.linalg.norm(a)), places=9)
            self.assertAlmostEqual(norm(list(a), p=1), float(np.linalg.norm(a, 1)), places=9)
            expected = float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
            self.assertAlmostEqual(cosine_similarity(list(a), list(b)), expected, places=9)

    def test_cosine_stays_in_range(self):
        rng = np.random.default_rng(1)
        for _ in range(20):
            a, b = rng.normal(size=8), rng.normal(size=8)
            c = cosine_similarity(list(a), list(b))
            self.assertGreaterEqual(c, -1 - 1e-12)
            self.assertLessEqual(c, 1 + 1e-12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
