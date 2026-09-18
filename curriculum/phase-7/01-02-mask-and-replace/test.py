import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import replace_outliers


def loop_version(x, k):
    out = x.copy()
    for j in range(x.shape[1]):
        col = x[:, j]
        mean, std, med = col.mean(), col.std(), np.median(col)
        for i in range(x.shape[0]):
            if abs(col[i] - mean) > k * std:
                out[i, j] = med
    return out


class TestReplaceOutliers(unittest.TestCase):
    def test_single_outlier_in_one_column(self):
        x = np.array([[1.0, 100.0], [2.0, 101.0], [3.0, 102.0], [4.0, 103.0], [50.0, 104.0]])
        expected = np.array([[1.0, 100.0], [2.0, 101.0], [3.0, 102.0], [4.0, 103.0], [3.0, 104.0]])
        assert_allclose(replace_outliers(x, 1.5), expected)

    def test_constant_column_has_no_outliers(self):
        x = np.ones((3, 1))
        assert_allclose(replace_outliers(x, 2.0), x)

    def test_exactly_k_stds_away_is_kept(self):
        x = np.array([[-1.0], [1.0]])  # mean 0, std 1: both are exactly 1 std away
        assert_allclose(replace_outliers(x, 1.0), x)
        assert_allclose(replace_outliers(x, 0.5), [[0.0], [0.0]])

    def test_uses_original_median_not_post_replacement(self):
        x = np.array([[0.0], [0.0], [10.0], [10.0], [1000.0]])
        result = replace_outliers(x, 1.0)
        self.assertAlmostEqual(result[4, 0], 10.0)

    def test_does_not_modify_input_and_returns_new_array(self):
        x = np.array([[1.0], [1.0], [1.0], [100.0]])
        result = replace_outliers(x, 1.0)
        self.assertIsNot(result, x)
        assert_allclose(x, [[1.0], [1.0], [1.0], [100.0]])
        self.assertAlmostEqual(result[3, 0], 1.0)

    def test_shape_and_dtype_preserved(self):
        x = np.arange(20.0).reshape(5, 4)
        result = replace_outliers(x, 3.0)
        self.assertEqual(result.shape, x.shape)
        self.assertEqual(result.dtype, x.dtype)

    def test_matches_loop_version_on_random_data(self):
        rng = np.random.default_rng(7)
        x = rng.normal(size=(300, 6))
        x[rng.integers(0, 300, 20), rng.integers(0, 6, 20)] += 40
        for k in (1.0, 2.0, 3.0):
            assert_allclose(replace_outliers(x, k), loop_version(x, k), atol=1e-9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
