import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import matmul, transpose


class TestMatmulLists(unittest.TestCase):
    def test_two_by_two(self):
        assert_allclose(matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]])

    def test_row_times_column_and_column_times_row(self):
        assert_allclose(matmul([[1, 2, 3]], [[1], [2], [3]]), [[14]])
        assert_allclose(matmul([[1], [2], [3]], [[1, 2, 3]]), [[1, 2, 3], [2, 4, 6], [3, 6, 9]])

    def test_result_shape(self):
        result = matmul([[1.0] * 4] * 3, [[1.0] * 5] * 4)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(len(row) == 5 for row in result))

    def test_inner_dimension_mismatch_raises(self):
        with self.assertRaises(ValueError):
            matmul([[1, 2]], [[1, 2]])
        with self.assertRaises(ValueError):
            matmul([[1, 2, 3]], [[1, 2], [3, 4]])

    def test_not_commutative(self):
        a, b = [[1, 2], [3, 4]], [[0, 1], [1, 0]]
        self.assertNotEqual(matmul(a, b), matmul(b, a))

    def test_identity_leaves_matrix_unchanged(self):
        a = [[1.5, -2.0], [0.0, 3.0]]
        assert_allclose(matmul(a, [[1, 0], [0, 1]]), a)

    def test_transpose(self):
        self.assertEqual(transpose([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]])
        self.assertEqual(transpose([[7]]), [[7]])
        self.assertEqual(transpose(transpose([[1, 2], [3, 4], [5, 6]])), [[1, 2], [3, 4], [5, 6]])

    def test_inputs_not_modified(self):
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        matmul(a, b)
        transpose(a)
        self.assertEqual(a, [[1, 2], [3, 4]])
        self.assertEqual(b, [[5, 6], [7, 8]])

    def test_matches_numpy_on_random_matrices(self):
        rng = np.random.default_rng(0)
        for m, n, p in [(3, 4, 5), (7, 2, 3), (1, 6, 1), (40, 30, 20)]:
            a = rng.normal(size=(m, n))
            b = rng.normal(size=(n, p))
            assert_allclose(matmul(a.tolist(), b.tolist()), a @ b, atol=1e-9)
            assert_allclose(transpose(a.tolist()), a.T)


if __name__ == "__main__":
    unittest.main(verbosity=2)
