import unittest

import numpy as np
import pandas as pd
import pandas.testing as pdt

from solution import Imputer, iqr_outlier_mask


def make_train():
    return pd.DataFrame({"a": [1.0, np.nan, 3.0, 5.0], "b": [10.0, 20.0, np.nan, 40.0]})


class TestImputerAndOutliers(unittest.TestCase):
    def test_transform_fills_with_train_medians_and_adds_indicators(self):
        test = pd.DataFrame({"a": [np.nan, 9.0], "b": [np.nan, 1.0]})
        out = Imputer().fit(make_train()).transform(test)
        expected = pd.DataFrame(
            {"a": [3.0, 9.0], "b": [20.0, 1.0], "a_missing": [True, False], "b_missing": [True, False]}
        )
        pdt.assert_frame_equal(out, expected)

    def test_fit_returns_self_and_transform_before_fit_raises(self):
        imp = Imputer()
        self.assertIs(imp.fit(make_train()), imp)
        with self.assertRaises(RuntimeError):
            Imputer().transform(make_train())

    def test_inputs_not_mutated(self):
        train, test = make_train(), pd.DataFrame({"a": [np.nan], "b": [np.nan]})
        t0, s0 = train.copy(), test.copy()
        Imputer().fit(train).transform(test)
        pdt.assert_frame_equal(train, t0)
        pdt.assert_frame_equal(test, s0)

    def test_medians_frozen_after_fit(self):
        imp = Imputer().fit(make_train())
        shifted = pd.DataFrame({"a": [1000.0, 2000.0, np.nan], "b": [np.nan, 5.0, 5.0]})
        out = imp.transform(shifted)
        self.assertAlmostEqual(out.loc[2, "a"], 3.0)
        self.assertAlmostEqual(out.loc[0, "b"], 20.0)

    def test_non_numeric_columns_copied_unchanged(self):
        train = pd.DataFrame({"a": [1.0, np.nan, 3.0], "name": ["x", "y", "z"]})
        out = Imputer().fit(train).transform(train)
        self.assertEqual(list(out.columns), ["a", "name", "a_missing"])
        self.assertEqual(out["name"].tolist(), ["x", "y", "z"])
        self.assertEqual(out["a_missing"].tolist(), [False, True, False])

    def test_iqr_outlier_mask_example(self):
        out = iqr_outlier_mask(pd.DataFrame({"x": [1, 2, 3, 4, 100]}))
        pdt.assert_frame_equal(out, pd.DataFrame({"x": [False, False, False, False, True]}))

    def test_iqr_mask_shape_nan_and_k(self):
        df = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0, np.nan, 30.0], "y": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]})
        out = iqr_outlier_mask(df)
        self.assertEqual(out.shape, df.shape)
        self.assertEqual(list(out.columns), ["x", "y"])
        self.assertTrue((out.dtypes == bool).all())
        self.assertFalse(out.loc[4, "x"])
        self.assertTrue(out.loc[5, "x"])
        self.assertFalse(out["y"].any())
        self.assertFalse(iqr_outlier_mask(df, k=100).to_numpy().any())

    def test_iqr_matches_numpy_random(self):
        rng = np.random.default_rng(0)
        df = pd.DataFrame(rng.standard_t(df=2, size=(5000, 3)), columns=list("abc"))
        out = iqr_outlier_mask(df, k=1.5)
        for col in df.columns:
            q1, q3 = np.percentile(df[col], [25, 75])
            iqr = q3 - q1
            expected = (df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)
            self.assertEqual(out[col].tolist(), expected.tolist())


if __name__ == "__main__":
    unittest.main(verbosity=2)
