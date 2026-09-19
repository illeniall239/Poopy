import unittest

from solution import (
    demographic_parity_difference,
    disparate_impact_ratio,
    equalized_odds_difference,
    passes_four_fifths,
)


def g(sel, tpr, fpr, **extra):
    return {"selection_rate": sel, "tpr": tpr, "fpr": fpr, **extra}


PARITY_BUT_UNEQUAL_ERRORS = {"a": g(0.5, 1.0, 0.0), "b": g(0.5, 0.5, 0.5)}
FAILS_FOUR_FIFTHS = {"a": g(0.5, 0.8, 0.2), "b": g(0.35, 0.7, 0.1)}


class TestFairnessMetrics(unittest.TestCase):
    def test_demographic_parity_difference(self):
        self.assertAlmostEqual(demographic_parity_difference(PARITY_BUT_UNEQUAL_ERRORS), 0.0)
        self.assertAlmostEqual(demographic_parity_difference(FAILS_FOUR_FIFTHS), 0.15)
        three = {"x": g(0.2, 0.5, 0.1), "y": g(0.6, 0.5, 0.1), "z": g(0.4, 0.5, 0.1)}
        self.assertAlmostEqual(demographic_parity_difference(three), 0.4)

    def test_equalized_odds_takes_the_larger_spread(self):
        self.assertAlmostEqual(equalized_odds_difference(PARITY_BUT_UNEQUAL_ERRORS), 0.5)
        # TPR spread 0.1, FPR spread 0.1 -> 0.1; now make the FPR spread dominate.
        self.assertAlmostEqual(equalized_odds_difference(FAILS_FOUR_FIFTHS), 0.1)
        m = {"a": g(0.3, 0.9, 0.05), "b": g(0.3, 0.85, 0.35), "c": g(0.3, 0.8, 0.2)}
        self.assertAlmostEqual(equalized_odds_difference(m), 0.3)

    def test_equalized_odds_undefined_group_raises(self):
        with self.assertRaises(ValueError):
            equalized_odds_difference({"a": g(0.5, None, 0.1), "b": g(0.5, 0.5, 0.1)})
        with self.assertRaises(ValueError):
            equalized_odds_difference({"a": g(0.5, 0.5, 0.1), "b": g(0.5, 0.5, None)})

    def test_disparate_impact_ratio(self):
        self.assertAlmostEqual(disparate_impact_ratio(FAILS_FOUR_FIFTHS), 0.7)
        self.assertAlmostEqual(disparate_impact_ratio(PARITY_BUT_UNEQUAL_ERRORS), 1.0)
        self.assertAlmostEqual(disparate_impact_ratio({"a": g(0.0, 0.5, 0.1), "b": g(0.4, 0.5, 0.1)}), 0.0)
        self.assertEqual(disparate_impact_ratio({"a": g(0.0, 0.5, 0.1), "b": g(0.0, 0.5, 0.1)}), 1.0)

    def test_four_fifths_rule_and_boundary(self):
        self.assertFalse(passes_four_fifths(FAILS_FOUR_FIFTHS))
        self.assertTrue(passes_four_fifths(PARITY_BUT_UNEQUAL_ERRORS))
        # 0.6 / 0.75 is 0.8 mathematically but 0.7999999999999999 in floating point.
        self.assertTrue(passes_four_fifths({"a": g(0.6, 0.5, 0.1), "b": g(0.75, 0.5, 0.1)}))
        self.assertFalse(passes_four_fifths({"a": g(0.59, 0.5, 0.1), "b": g(0.75, 0.5, 0.1)}))

    def test_selection_rate_metrics_ignore_undefined_error_rates_and_extra_keys(self):
        m = {"a": g(0.4, None, 0.1, n=10, accuracy=0.9), "b": g(0.5, 0.6, None, n=3, accuracy=0.2)}
        self.assertAlmostEqual(demographic_parity_difference(m), 0.1)
        self.assertAlmostEqual(disparate_impact_ratio(m), 0.8)
        self.assertTrue(passes_four_fifths(m))

    def test_fewer_than_two_groups_raises(self):
        one = {"a": g(0.5, 0.5, 0.5)}
        for fn in (demographic_parity_difference, equalized_odds_difference, disparate_impact_ratio, passes_four_fifths):
            with self.assertRaises(ValueError):
                fn(one)
            with self.assertRaises(ValueError):
                fn({})


if __name__ == "__main__":
    unittest.main(verbosity=2)
