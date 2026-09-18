import unittest

import numpy as np

from solution import determinant


class TestDeterminant(unittest.TestCase):
    def test_one_by_one_and_two_by_two(self):
        self.assertAlmostEqual(determinant([[2]]), 2.0)
        self.assertAlmostEqual(determinant([[1, 2], [3, 4]]), -2.0)

    def test_diagonal(self):
        self.assertAlmostEqual(determinant([[2, 0, 0], [0, 3, 0], [0, 0, 4]]), 24.0)

    def test_swap_flips_sign(self):
        self.assertAlmostEqual(determinant([[0, 1], [1, 0]]), -1.0)
        self.assertAlmostEqual(determinant([[0, 0, 1], [0, 1, 0], [1, 0, 0]]), -1.0)
        self.assertAlmostEqual(determinant([[0, 1, 0], [0, 0, 1], [1, 0, 0]]), 1.0)

    def test_singular_is_zero(self):
        self.assertAlmostEqual(determinant([[1, 2], [2, 4]]), 0.0)
        self.assertAlmostEqual(determinant([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), 0.0, places=9)

    def test_not_square_raises(self):
        with self.assertRaises(ValueError):
            determinant([[1, 2, 3]])
        with self.assertRaises(ValueError):
            determinant([[1, 2], [3]])

    def test_input_unchanged(self):
        a = [[4, 3], [6, 3]]
        determinant(a)
        self.assertEqual(a, [[4, 3], [6, 3]])

    def test_tiny_first_pivot_needs_pivoting(self):
        a = [[1e-17, 1.0], [1.0, 1.0]]
        self.assertAlmostEqual(determinant(a), float(np.linalg.det(np.array(a))), places=9)

    def test_matches_numpy_random(self):
        rng = np.random.default_rng(0)
        for n in [3, 5, 8, 15, 30]:
            a = rng.normal(size=(n, n))
            expected = float(np.linalg.det(a))
            self.assertAlmostEqual(determinant(a.tolist()) / expected, 1.0, delta=1e-6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
