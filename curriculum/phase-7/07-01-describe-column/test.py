import math
import unittest

import numpy as np
import pandas as pd
import pandas.testing as pdt

from solution import describe_column

KEYS = ["count", "missing", "mean", "median", "std", "skewness", "min", "max"]


def expected_from_numpy(values, missing):
    x = np.asarray(values, float)
    n = len(x)
    m = x.mean()
    m2 = ((x - m) ** 2).mean()
    m3 = ((x - m) ** 3).mean()
    skew = math.sqrt(n * (n - 1)) / (n - 2) * m3 / m2**1.5 if n >= 3 and m2 > 0 else float("nan")
    std = x.std(ddof=1) if n >= 2 else float("nan")
    return pd.Series([n, missing, m, np.median(x), std, skew, x.min(), x.max()], index=KEYS, dtype=float)


class TestDescribeColumn(unittest.TestCase):
    def test_example(self):
        out = describe_column(pd.Series([1.0, 2.0, np.nan, 4.0, 100.0]))
        self.assertEqual(list(out.index), KEYS)
        pdt.assert_series_equal(out, expected_from_numpy([1.0, 2.0, 4.0, 100.0], 1), rtol=1e-9)

    def test_no_missing(self):
        vals = [3.0, 1.0, 2.0, 5.0, 4.0]
        out = describe_column(pd.Series(vals))
        self.assertAlmostEqual(out["missing"], 0)
        self.assertAlmostEqual(out["median"], 3.0)
        self.assertAlmostEqual(out["skewness"], 0.0, places=9)

    def test_single_value_nan_std_and_skew(self):
        out = describe_column(pd.Series([3.0, np.nan]))
        self.assertAlmostEqual(out["count"], 1)
        self.assertAlmostEqual(out["missing"], 1)
        self.assertAlmostEqual(out["mean"], 3.0)
        self.assertTrue(math.isnan(out["std"]))
        self.assertTrue(math.isnan(out["skewness"]))

    def test_two_values_skew_nan(self):
        out = describe_column(pd.Series([1.0, 3.0]))
        self.assertAlmostEqual(out["std"], math.sqrt(2))
        self.assertTrue(math.isnan(out["skewness"]))

    def test_all_missing_raises(self):
        with self.assertRaises(ValueError):
            describe_column(pd.Series([np.nan, np.nan]))

    def test_input_unchanged(self):
        s = pd.Series([1.0, np.nan, 2.0])
        before = s.copy()
        describe_column(s)
        pdt.assert_series_equal(s, before)

    def test_result_is_float_series(self):
        out = describe_column(pd.Series([1, 2, 3]))
        self.assertIsInstance(out, pd.Series)
        self.assertTrue(pd.api.types.is_float_dtype(out))

    def test_matches_numpy_random_with_nans(self):
        rng = np.random.default_rng(0)
        vals = rng.lognormal(size=10_000)
        mask = rng.random(10_000) < 0.1
        s = pd.Series(np.where(mask, np.nan, vals))
        pdt.assert_series_equal(describe_column(s), expected_from_numpy(vals[~mask], int(mask.sum())), rtol=1e-9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
