import unittest

import numpy as np
from matplotlib import cbook

from solution import boxplot_summary


class TestBoxplotSummary(unittest.TestCase):
    def test_example_with_outlier(self):
        s = boxplot_summary([1, 2, 3, 4, 5, 6, 7, 8, 9, 30])
        self.assertAlmostEqual(s["q1"], 3.25)
        self.assertAlmostEqual(s["median"], 5.5)
        self.assertAlmostEqual(s["q3"], 7.75)
        self.assertAlmostEqual(s["iqr"], 4.5)
        self.assertAlmostEqual(s["whisker_low"], 1)
        self.assertAlmostEqual(s["whisker_high"], 9)
        self.assertEqual(s["outliers"], [30])

    def test_single_value(self):
        s = boxplot_summary([5])
        for key in ["q1", "median", "q3", "whisker_low", "whisker_high"]:
            self.assertAlmostEqual(s[key], 5)
        self.assertAlmostEqual(s["iqr"], 0)
        self.assertEqual(s["outliers"], [])

    def test_unsorted_input_and_interpolation(self):
        s = boxplot_summary([4, 1, 3, 2])
        self.assertAlmostEqual(s["q1"], 1.75)
        self.assertAlmostEqual(s["median"], 2.5)
        self.assertAlmostEqual(s["q3"], 3.25)

    def test_input_unchanged(self):
        vals = [4, 1, 3, 2]
        boxplot_summary(vals)
        self.assertEqual(vals, [4, 1, 3, 2])

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            boxplot_summary([])

    def test_whiskers_are_data_points(self):
        vals = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, -40, 80]
        s = boxplot_summary(vals)
        self.assertIn(s["whisker_low"], vals)
        self.assertIn(s["whisker_high"], vals)
        self.assertEqual(sorted(s["outliers"]), [-40, 80])

    def test_outliers_keep_original_order(self):
        s = boxplot_summary([100, 1, 2, 3, 4, 5, 6, 7, 8, -100])
        self.assertEqual(s["outliers"], [100, -100])

    def test_matches_matplotlib_random(self):
        rng = np.random.default_rng(0)
        for n in [5, 20, 101, 2000]:
            vals = np.concatenate([rng.normal(size=n), rng.normal(scale=6, size=max(1, n // 20))]).tolist()
            s = boxplot_summary(vals)
            (m,) = cbook.boxplot_stats(vals)
            self.assertAlmostEqual(s["q1"], m["q1"], places=9)
            self.assertAlmostEqual(s["median"], m["med"], places=9)
            self.assertAlmostEqual(s["q3"], m["q3"], places=9)
            self.assertAlmostEqual(s["iqr"], m["iqr"], places=9)
            self.assertAlmostEqual(s["whisker_low"], m["whislo"], places=9)
            self.assertAlmostEqual(s["whisker_high"], m["whishi"], places=9)
            np.testing.assert_allclose(sorted(s["outliers"]), sorted(m["fliers"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
