import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import solve


class TestSolveGaussian(unittest.TestCase):
    def test_diagonal(self):
        assert_allclose(solve([[2, 0], [0, 4]], [2, 8]), [1.0, 2.0])

    def test_two_by_two(self):
        assert_allclose(solve([[1, 1], [1, -1]], [3, 1]), [2.0, 1.0])

    def test_needs_swap(self):
        assert_allclose(solve([[0, 1], [1, 0]], [5, 7]), [7.0, 5.0])

    def test_three_by_three(self):
        a = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
        assert_allclose(solve(a, [8, -11, -3]), [2.0, 3.0, -1.0], atol=1e-9)

    def test_singular_raises(self):
        with self.assertRaises(ValueError):
            solve([[1, 2], [2, 4]], [3, 6])
        with self.assertRaises(ValueError):
            solve([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 1, 1])

    def test_shape_mismatch_raises(self):
        with self.assertRaises(ValueError):
            solve([[1, 2], [3, 4]], [1, 2, 3])
        with self.assertRaises(ValueError):
            solve([[1, 2, 3], [4, 5, 6]], [1, 2])

    def test_inputs_unchanged(self):
        a, b = [[0, 1], [1, 0]], [5, 7]
        solve(a, b)
        self.assertEqual(a, [[0, 1], [1, 0]])
        self.assertEqual(b, [5, 7])

    def test_tiny_pivot_handled_by_pivoting(self):
        a = [[1e-17, 1.0], [1.0, 1.0]]
        assert_allclose(solve(a, [1.0, 2.0]), np.linalg.solve(np.array(a), [1.0, 2.0]), atol=1e-9)

    def test_matches_numpy_random(self):
        rng = np.random.default_rng(0)
        for n in [3, 6, 12, 40]:
            a = rng.normal(size=(n, n)) + n * np.eye(n)
            b = rng.normal(size=n)
            x = solve(a.tolist(), b.tolist())
            self.assertEqual(len(x), n)
            assert_allclose(x, np.linalg.solve(a, b), atol=1e-8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
