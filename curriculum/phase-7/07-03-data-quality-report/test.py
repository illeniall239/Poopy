import unittest

import numpy as np
import pandas as pd
import pandas.testing as pdt

from solution import quality_report


def make_tables():
    train = pd.DataFrame(
        {
            "id": [1, 2, 3, 3],
            "const": [7, 7, 7, 7],
            "x": [1.0, 2.0, 3.0, 3.0],
            "y": [np.nan, 2.0, 3.0, 3.0],
            "label": [0, 1, 0, 0],
        }
    )
    test = pd.DataFrame({"id": [10, 11], "const": [7, 7], "x": [50.0, 51.0], "y": [1.0, 2.0], "label": [1, 0]})
    return train, test


class TestDataQualityReport(unittest.TestCase):
    def test_example(self):
        r = quality_report(*make_tables(), k=3)
        self.assertEqual(r["duplicate_rows"], 1)
        self.assertIsInstance(r["duplicate_rows"], int)
        pdt.assert_series_equal(
            r["missing_rate"],
            pd.Series([0.0, 0.0, 0.0, 0.25, 0.0], index=["id", "const", "x", "y", "label"]),
            rtol=1e-9,
            check_names=False,
        )
        self.assertEqual(r["constant_columns"], ["const"])
        self.assertEqual(r["id_like_columns"], [])
        self.assertEqual(r["drifted_columns"], ["id", "x"])

    def test_id_like_detected_without_duplicate(self):
        train, test = make_tables()
        train = train.iloc[:3]
        r = quality_report(train, test)
        self.assertEqual(r["duplicate_rows"], 0)
        self.assertEqual(r["id_like_columns"], ["id", "x", "y"])

    def test_all_nan_column_is_constant_not_id(self):
        train, test = make_tables()
        train = train.assign(empty=np.nan)
        test = test.assign(empty=np.nan)
        r = quality_report(train, test)
        self.assertIn("empty", r["constant_columns"])
        self.assertNotIn("empty", r["id_like_columns"])
        self.assertNotIn("empty", r["drifted_columns"])
        self.assertAlmostEqual(r["missing_rate"]["empty"], 1.0)

    def test_constant_column_never_drifts(self):
        train, test = make_tables()
        test = test.assign(const=[8, 8])
        self.assertNotIn("const", quality_report(train, test)["drifted_columns"])

    def test_text_columns_skipped_in_drift(self):
        train, test = make_tables()
        train = train.assign(city=["a", "b", "c", "d"])
        test = test.assign(city=["zz", "zz"])
        r = quality_report(train, test)
        self.assertNotIn("city", r["drifted_columns"])
        self.assertIn("city", r["id_like_columns"])

    def test_k_controls_drift(self):
        train, test = make_tables()
        self.assertIn("x", quality_report(train, test, k=3)["drifted_columns"])
        self.assertNotIn("x", quality_report(train, test, k=1000)["drifted_columns"])

    def test_inputs_not_modified(self):
        train, test = make_tables()
        t0, s0 = train.copy(), test.copy()
        quality_report(train, test)
        pdt.assert_frame_equal(train, t0)
        pdt.assert_frame_equal(test, s0)

    def test_random_drift_matches_manual(self):
        rng = np.random.default_rng(0)
        cols = list("abcde")
        train = pd.DataFrame(rng.normal(size=(2000, 5)), columns=cols)
        test = pd.DataFrame(rng.normal(size=(500, 5)), columns=cols)
        test["c"] += 5.0
        test["e"] -= 4.0
        r = quality_report(train, test, k=3)
        self.assertEqual(r["drifted_columns"], ["c", "e"])
        self.assertEqual(r["id_like_columns"], cols)
        self.assertEqual(r["constant_columns"], [])
        pdt.assert_series_equal(r["missing_rate"], pd.Series(0.0, index=cols), check_names=False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
