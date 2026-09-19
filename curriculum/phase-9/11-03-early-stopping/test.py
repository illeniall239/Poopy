import unittest

from solution import early_stopping_epoch

CURVE = [1.0, 0.8, 0.7, 0.75, 0.72, 0.71]


class TestEarlyStopping(unittest.TestCase):
    def test_stops_and_restores_best(self):
        self.assertEqual(early_stopping_epoch(CURVE, 3), 2)

    def test_returns_none_when_never_stalled(self):
        self.assertIsNone(early_stopping_epoch(CURVE, 4))
        self.assertIsNone(early_stopping_epoch([3.0, 2.0, 1.0, 0.5], 1))

    def test_ties_are_not_improvement(self):
        self.assertEqual(early_stopping_epoch([0.5, 0.5, 0.5], 2), 0)

    def test_stops_before_a_later_improvement(self):
        self.assertEqual(early_stopping_epoch([1.0, 0.9, 0.95, 0.96, 0.5], 2), 1)

    def test_counter_resets_on_improvement(self):
        # stalls for 2, improves, stalls for 2, improves: patience 3 is never reached
        self.assertIsNone(early_stopping_epoch([1.0, 1.1, 1.2, 0.9, 1.0, 1.0, 0.8], 3))
        self.assertEqual(early_stopping_epoch([1.0, 1.1, 1.2, 0.9, 1.0, 1.0, 0.8], 2), 0)

    def test_patience_one(self):
        self.assertEqual(early_stopping_epoch([2.0, 1.0, 1.5, 0.1], 1), 1)

    def test_empty_and_single(self):
        self.assertIsNone(early_stopping_epoch([], 3))
        self.assertIsNone(early_stopping_epoch([0.3], 1))

    def test_rejects_bad_patience(self):
        with self.assertRaises(ValueError):
            early_stopping_epoch(CURVE, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
