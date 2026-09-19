import unittest

from solution import diagnose


class TestDiagnose(unittest.TestCase):
    def test_avoidable_bias(self):
        self.assertEqual(diagnose(0.01, 0.08, 0.09, 0.10, 0.10), "avoidable bias")
        self.assertEqual(diagnose(0.0, 0.30, 0.31, 0.32, 0.33), "avoidable bias")

    def test_variance(self):
        self.assertEqual(diagnose(0.01, 0.015, 0.08, 0.09, 0.09), "variance")

    def test_data_mismatch(self):
        self.assertEqual(diagnose(0.01, 0.015, 0.02, 0.10, 0.10), "data mismatch")

    def test_dev_overfitting(self):
        self.assertEqual(diagnose(0.01, 0.02, 0.03, 0.04, 0.12), "dev overfitting")

    def test_exact_ties_follow_the_table_order(self):
        self.assertEqual(diagnose(0.0, 0.25, 0.5, 0.5, 0.5), "avoidable bias")
        self.assertEqual(diagnose(0.0, 0.0, 0.25, 0.5, 0.5), "variance")
        self.assertEqual(diagnose(0.0, 0.0, 0.0, 0.25, 0.5), "data mismatch")

    def test_floating_point_near_ties_count_as_ties(self):
        # 0.3 - 0.2 = 0.09999999999999998 but 0.4 - 0.3 = 0.10000000000000003: still a tie.
        self.assertEqual(diagnose(0.2, 0.3, 0.4, 0.4, 0.4), "avoidable bias")
        # 0.8 - 0.7 = 0.10000000000000009 beats 0.7 - 0.6 = 0.09999999999999998 only by rounding.
        self.assertEqual(diagnose(0.6, 0.6, 0.7, 0.8, 0.8), "variance")
        self.assertEqual(diagnose(0.1, 0.2, 0.3, 0.3, 0.3), "avoidable bias")
        # A later gap that is clearly larger still wins.
        self.assertEqual(diagnose(0.1, 0.2, 0.3000001, 0.3000001, 0.3000001), "variance")

    def test_negative_gaps_are_allowed(self):
        # train-dev below train and test below dev: only data mismatch is positive.
        self.assertEqual(diagnose(0.05, 0.04, 0.03, 0.09, 0.08), "data mismatch")
        self.assertEqual(diagnose(0.1, 0.05, 0.04, 0.03, 0.02), "variance")

    def test_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            diagnose(0.01, 0.08, 0.09, 0.10, 1.2)
        with self.assertRaises(ValueError):
            diagnose(-0.01, 0.08, 0.09, 0.10, 0.1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
