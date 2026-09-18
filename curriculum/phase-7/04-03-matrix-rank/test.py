import unittest

import numpy as np

from solution import is_singular, matrix_rank


class TestMatrixRank(unittest.TestCase):
    def test_identity_and_dependent_rows(self):
        self.assertEqual(matrix_rank([[1, 0], [0, 1]]), 2)
        self.assertEqual(matrix_rank([[1, 2], [2, 4]]), 1)
        self.assertEqual(matrix_rank([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), 2)

    def test_duplicated_column(self):
        self.assertEqual(matrix_rank([[1, 2, 1], [3, 4, 3], [5, 6, 5]]), 2)

    def test_rectangular(self):
        self.assertEqual(matrix_rank([[1, 2, 3], [4, 5, 6]]), 2)
        self.assertEqual(matrix_rank([[1, 2], [2, 4], [3, 6]]), 1)
        self.assertEqual(matrix_rank([[0, 0, 1], [0, 0, 2]]), 1)

    def test_zero_matrix(self):
        self.assertEqual(matrix_rank([[0, 0], [0, 0]]), 0)

    def test_input_unchanged(self):
        a = [[1, 2], [3, 4]]
        matrix_rank(a)
        self.assertEqual(a, [[1, 2], [3, 4]])

    def test_is_singular(self):
        self.assertTrue(is_singular([[1, 2], [2, 4]]))
        self.assertFalse(is_singular([[1, 2], [3, 4]]))
        with self.assertRaises(ValueError):
            is_singular([[1, 2, 3]])

    def test_near_dependence_respects_tolerance(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=(20, 4))
        fifth = x.sum(axis=1) + rng.normal(scale=1e-13, size=20)
        a = np.column_stack([x, fifth]).tolist()
        self.assertEqual(matrix_rank(a), 4)
        self.assertEqual(matrix_rank(a), int(np.linalg.matrix_rank(np.array(a), tol=1e-9)))
        self.assertEqual(matrix_rank(a, tol=0.0), 5)

    def test_matches_numpy_random(self):
        rng = np.random.default_rng(1)
        for m, n, r in [(6, 6, 3), (10, 4, 4), (8, 12, 5), (40, 40, 40)]:
            a = rng.normal(size=(m, r)) @ rng.normal(size=(r, n))
            self.assertEqual(matrix_rank(a.tolist()), int(np.linalg.matrix_rank(a)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
