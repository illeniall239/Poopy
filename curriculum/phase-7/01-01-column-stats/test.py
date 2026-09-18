import time
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import column_stats


class TestColumnStats(unittest.TestCase):
    def test_small_matrix(self):
        x = np.array([[1.0, 10.0], [3.0, 30.0], [5.0, 50.0]])
        stats = column_stats(x)
        assert_allclose(stats["mean"], [3.0, 30.0])
        assert_allclose(stats["std"], [np.sqrt(8 / 3), 10 * np.sqrt(8 / 3)])
        assert_allclose(stats["min"], [1.0, 10.0])
        assert_allclose(stats["max"], [5.0, 50.0])

    def test_has_exactly_the_four_keys(self):
        stats = column_stats(np.ones((2, 3)))
        self.assertEqual(set(stats), {"mean", "std", "min", "max"})

    def test_shapes_are_per_column_not_per_row(self):
        x = np.arange(12.0).reshape(4, 3)
        for key, value in column_stats(x).items():
            self.assertEqual(value.shape, (3,), key)

    def test_single_row_has_zero_std(self):
        stats = column_stats(np.array([[7.0, -2.0]]))
        assert_allclose(stats["std"], [0.0, 0.0])
        assert_allclose(stats["mean"], [7.0, -2.0])

    def test_std_is_population_std(self):
        x = np.array([[1.0], [2.0], [3.0], [4.0]])
        assert_allclose(column_stats(x)["std"], [np.std([1, 2, 3, 4], ddof=0)])

    def test_matches_numpy_on_random_data(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=(500, 7)) * 3 + 1
        stats = column_stats(x)
        assert_allclose(stats["mean"], x.mean(axis=0), atol=1e-9)
        assert_allclose(stats["std"], x.std(axis=0), atol=1e-9)
        assert_allclose(stats["min"], x.min(axis=0))
        assert_allclose(stats["max"], x.max(axis=0))

    def test_does_not_change_input(self):
        x = np.array([[1.0, 2.0], [3.0, 4.0]])
        column_stats(x)
        assert_allclose(x, [[1.0, 2.0], [3.0, 4.0]])

    def test_large_array_is_fast(self):
        rng = np.random.default_rng(1)
        x = rng.random((200_000, 50))
        start = time.perf_counter()
        stats = column_stats(x)
        self.assertLess(time.perf_counter() - start, 2.0)
        assert_allclose(stats["mean"], x.mean(axis=0), atol=1e-9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
