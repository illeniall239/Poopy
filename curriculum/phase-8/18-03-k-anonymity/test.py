import copy
import unittest

from solution import generalize, k_anonymity


def records():
    return [
        {"age": 34, "zip": "13053", "disease": "flu"},
        {"age": 36, "zip": "13068", "disease": "cold"},
        {"age": 38, "zip": "13053", "disease": "flu"},
        {"age": 52, "zip": "14850", "disease": "asthma"},
        {"age": 57, "zip": "14853", "disease": "flu"},
        {"age": 55, "zip": "14850", "disease": "cold"},
    ]


def decade(a):
    return f"{a // 10 * 10}-{a // 10 * 10 + 9}"


RULES = {"age": [decade], "zip": [lambda z: z[:3] + "**"]}
QIDS = ["age", "zip"]


class TestKAnonymity(unittest.TestCase):
    def test_k_anonymity_counts_the_smallest_class(self):
        self.assertEqual(k_anonymity(records(), QIDS), 1)
        self.assertEqual(k_anonymity(records(), ["zip"]), 1)
        self.assertEqual(k_anonymity(records(), []), 6)
        rows = [{"a": 1, "b": 2}, {"a": 1, "b": 2}, {"a": 1, "b": 3}, {"a": 1, "b": 3}, {"a": 1, "b": 3}]
        self.assertEqual(k_anonymity(rows, ["a", "b"]), 2)
        self.assertEqual(k_anonymity(rows, ["a"]), 5)

    def test_k_anonymity_rejects_empty(self):
        with self.assertRaises(ValueError):
            k_anonymity([], QIDS)

    def test_generalize_to_three(self):
        out = generalize(records(), QIDS, RULES, 3)
        self.assertEqual(out, [
            {"age": "30-39", "zip": "130**", "disease": "flu"},
            {"age": "30-39", "zip": "130**", "disease": "cold"},
            {"age": "30-39", "zip": "130**", "disease": "flu"},
            {"age": "50-59", "zip": "148**", "disease": "asthma"},
            {"age": "50-59", "zip": "148**", "disease": "flu"},
            {"age": "50-59", "zip": "148**", "disease": "cold"},
        ])
        self.assertGreaterEqual(k_anonymity(out, QIDS), 3)

    def test_stops_as_soon_as_k_is_reached(self):
        self.assertEqual(generalize(records(), QIDS, RULES, 1), records())
        # Only zip needs coarsening when zip is the sole quasi-identifier and k = 3.
        out = generalize(records(), ["zip"], RULES, 3)
        self.assertEqual([r["zip"] for r in out], ["130**"] * 3 + ["148**"] * 3)
        self.assertEqual([r["age"] for r in out], [34, 36, 38, 52, 57, 55])

    def test_lowest_level_first_then_quasi_id_order(self):
        # Age first (tie at level 0, earliest), then zip; age masked before zip on the next tie.
        out = generalize(records(), QIDS, RULES, 4)
        self.assertEqual({(r["age"], r["zip"]) for r in out}, {("*", "*")})
        out = generalize(records(), ["zip", "age"], RULES, 2)
        # zip goes first now: zip to 3 digits alone gives classes of 1, so age is raised next.
        self.assertEqual([(r["age"], r["zip"]) for r in out][:2], [("30-39", "130**"), ("30-39", "130**")])

    def test_levels_apply_to_the_original_value(self):
        # Level 2 needs the original age; applied to "20-29" it would fail or misbin.
        rules = {"age": [decade, lambda a: "young" if a < 45 else "old"]}
        rows = [{"age": a} for a in (21, 29, 31, 38, 52, 58, 61)]
        out = generalize(rows, ["age"], rules, 3)
        self.assertEqual([r["age"] for r in out], ["young"] * 4 + ["old"] * 3)
        out = generalize(rows[:6], ["age"], rules, 2)
        self.assertEqual([r["age"] for r in out], ["20-29", "20-29", "30-39", "30-39", "50-59", "50-59"])

    def test_column_without_rules_is_masked_directly(self):
        rows = [{"sex": "F", "zip": "1"}, {"sex": "M", "zip": "1"}, {"sex": "F", "zip": "1"}]
        self.assertEqual(generalize(rows, ["sex", "zip"], {}, 2), [{"sex": "*", "zip": "1"}] * 3)

    def test_input_is_not_modified(self):
        original = records()
        snapshot = copy.deepcopy(original)
        generalize(original, QIDS, RULES, 4)
        self.assertEqual(original, snapshot)

    def test_rejects_impossible_and_bad_input(self):
        with self.assertRaises(ValueError):
            generalize(records(), QIDS, RULES, 7)
        with self.assertRaises(ValueError):
            generalize(records(), QIDS, RULES, 0)
        with self.assertRaises(ValueError):
            generalize([], QIDS, RULES, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
