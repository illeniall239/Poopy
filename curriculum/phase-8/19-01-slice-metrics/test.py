import unittest

from solution import slice_metrics, worst_errors


def acc(t, p):
    return sum(a == b for a, b in zip(t, p)) / len(t)


class TestSliceMetrics(unittest.TestCase):
    def test_hand_computed_slices(self):
        out = slice_metrics([1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 1, 1], ["web", "web", "app", "app", "app", "web"], acc)
        self.assertEqual([(v, n) for v, _, n in out], [("app", 3), ("web", 3)])
        self.assertAlmostEqual(out[0][1], 1 / 3)
        self.assertAlmostEqual(out[1][1], 1.0)

    def test_high_overall_accuracy_hides_a_bad_slice(self):
        # 90% overall; the rare "night" slice is at 50%.
        y_true = [1] * 100
        y_pred = [1] * 85 + [0] * 5 + [1] * 5 + [0] * 5
        when = ["day"] * 90 + ["night"] * 10
        self.assertAlmostEqual(acc(y_true, y_pred), 0.9)
        out = slice_metrics(y_true, y_pred, when, acc)
        self.assertEqual(out[0][0], "night")
        self.assertAlmostEqual(out[0][1], 0.5)
        self.assertEqual(out[0][2], 10)
        self.assertEqual(out[1][2], 90)

    def test_ties_keep_first_appearance_and_metric_called_per_slice(self):
        calls = []

        def counting(t, p):
            calls.append(len(t))
            return acc(t, p)

        out = slice_metrics([1, 1, 1, 1, 0], [1, 1, 1, 1, 1], ["z", "a", "m", "a", "q"], counting)
        self.assertEqual([v for v, _, _ in out], ["q", "z", "a", "m"])
        self.assertEqual(sorted(calls), [1, 1, 1, 2])

    def test_passes_slice_lists_in_row_order(self):
        seen = {}

        def record(t, p):
            seen[tuple(t)] = tuple(p)
            return 0.0

        slice_metrics([1, 2, 3, 4], [5, 6, 7, 8], [0, 1, 0, 1], record)
        self.assertEqual(seen, {(1, 3): (5, 7), (2, 4): (6, 8)})

    def test_slice_metrics_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            slice_metrics([], [], [], acc)
        with self.assertRaises(ValueError):
            slice_metrics([1, 0], [1], ["a", "b"], acc)

    def test_worst_errors_hand_computed(self):
        self.assertEqual(worst_errors([1, 0, 1, 0, 1], [0.05, 0.4, 0.45, 0.98, 0.9], 2), [3, 0])
        self.assertEqual(worst_errors([1, 0, 1, 0, 1], [0.05, 0.4, 0.45, 0.98, 0.9], 10), [3, 0, 2])
        self.assertEqual(worst_errors([1, 0], [0.9, 0.1], 5), [])
        self.assertEqual(worst_errors([1, 0], [0.1, 0.9], 0), [])

    def test_worst_errors_threshold_and_ties(self):
        # 0.5 predicts 1, so a true 0 at 0.5 is a mistake (confidence 0); a true 1 at 0.5 is not.
        self.assertEqual(worst_errors([0, 1], [0.5, 0.5], 5), [0])
        self.assertEqual(worst_errors([0, 1, 0, 1], [0.75, 0.25, 0.75, 0.25], 3), [0, 1, 2])

    def test_worst_errors_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            worst_errors([1, 0], [0.2], 1)
        with self.assertRaises(ValueError):
            worst_errors([1], [0.2], -1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
