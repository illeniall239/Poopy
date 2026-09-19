import unittest

from solution import improvement_over_baseline, keyword_classify, rule_accuracy

KW = {"spam": ["free", "winner", "prize"], "ham": ["meeting", "lunch"]}


class TestHeuristicBaseline(unittest.TestCase):
    def test_counts_hits_case_insensitively(self):
        self.assertEqual(keyword_classify("FREE prize inside", KW, "ham"), "spam")
        self.assertEqual(keyword_classify("Lunch meeting, free pizza", KW, "ham"), "ham")

    def test_every_occurrence_counts(self):
        self.assertEqual(keyword_classify("free free free, lunch meeting", KW, "x"), "spam")

    def test_tie_goes_to_first_label_and_no_hit_to_default(self):
        self.assertEqual(keyword_classify("free lunch", KW, "other"), "spam")
        swapped = {"ham": KW["ham"], "spam": KW["spam"]}
        self.assertEqual(keyword_classify("free lunch", swapped, "other"), "ham")
        self.assertEqual(keyword_classify("nothing to see here", KW, "other"), "other")
        self.assertEqual(keyword_classify("", KW, "other"), "other")

    def test_whole_words_only(self):
        self.assertEqual(keyword_classify("Freedom!", KW, "other"), "other")
        self.assertEqual(keyword_classify("prizes and winners", KW, "other"), "other")
        self.assertEqual(keyword_classify("free-prize", KW, "other"), "spam")

    def test_rule_accuracy(self):
        texts = ["Free prize!", "lunch at noon", "team meeting", "you are a WINNER", "hello"]
        labels = ["spam", "ham", "ham", "ham", "spam"]
        self.assertAlmostEqual(rule_accuracy(texts, labels, KW, "ham"), 3 / 5)
        with self.assertRaises(ValueError):
            rule_accuracy([], [], KW, "ham")
        with self.assertRaises(ValueError):
            rule_accuracy(["a"], ["spam", "ham"], KW, "ham")

    def test_improvement_is_relative_error_reduction(self):
        self.assertAlmostEqual(improvement_over_baseline(0.95, 0.90), 0.5, places=9)
        self.assertAlmostEqual(improvement_over_baseline(0.92, 0.90), 0.2, places=9)
        self.assertAlmostEqual(improvement_over_baseline(1.0, 0.5), 1.0, places=9)
        self.assertAlmostEqual(improvement_over_baseline(0.6, 0.6), 0.0, places=9)

    def test_improvement_is_negative_when_worse(self):
        self.assertAlmostEqual(improvement_over_baseline(0.85, 0.90), -0.5, places=9)
        self.assertAlmostEqual(improvement_over_baseline(0.0, 0.5), -1.0, places=9)

    def test_improvement_rejects_bad_scores(self):
        with self.assertRaises(ValueError):
            improvement_over_baseline(0.9, 1.0)
        with self.assertRaises(ValueError):
            improvement_over_baseline(1.2, 0.5)
        with self.assertRaises(ValueError):
            improvement_over_baseline(0.5, -0.1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
