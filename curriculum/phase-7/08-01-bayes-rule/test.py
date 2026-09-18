import unittest

from solution import bayes, posterior_positive_test


class TestBayesRule(unittest.TestCase):
    def test_bayes_basic(self):
        self.assertAlmostEqual(bayes(0.5, 0.8, 0.4), 1.0)
        self.assertAlmostEqual(bayes(0.01, 0.9, 0.1), 0.09)
        self.assertAlmostEqual(bayes(0.3, 0.5, 0.5), 0.3)

    def test_bayes_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            bayes(0.5, 0.9, 0.0)
        with self.assertRaises(ValueError):
            bayes(1.5, 0.9, 0.5)
        with self.assertRaises(ValueError):
            bayes(0.5, -0.1, 0.5)
        with self.assertRaises(ValueError):
            bayes(0.9, 0.9, 0.1)

    def test_rare_condition_accurate_test(self):
        self.assertAlmostEqual(posterior_positive_test(0.01, 0.99, 0.99), 0.5)

    def test_common_condition(self):
        self.assertAlmostEqual(posterior_positive_test(0.5, 0.99, 0.99), 0.99)

    def test_edge_prevalences(self):
        self.assertAlmostEqual(posterior_positive_test(0.0, 0.99, 0.99), 0.0)
        self.assertAlmostEqual(posterior_positive_test(1.0, 0.99, 0.99), 1.0)

    def test_specificity_matters(self):
        loose = posterior_positive_test(0.05, 0.95, 0.80)
        tight = posterior_positive_test(0.05, 0.95, 0.99)
        self.assertLess(loose, tight)
        self.assertAlmostEqual(loose, 0.95 * 0.05 / (0.95 * 0.05 + 0.20 * 0.95))

    def test_counting_argument(self):
        # 10 000 people, 2% sick, sensitivity 0.9, specificity 0.95
        sick, healthy = 200, 9800
        tp, fp = 0.9 * sick, 0.05 * healthy
        self.assertAlmostEqual(posterior_positive_test(0.02, 0.9, 0.95), tp / (tp + fp))

    def test_posterior_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            posterior_positive_test(-0.1, 0.9, 0.9)
        with self.assertRaises(ValueError):
            posterior_positive_test(0.1, 1.2, 0.9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
