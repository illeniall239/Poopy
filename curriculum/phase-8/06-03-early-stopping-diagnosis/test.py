import unittest

from solution import diagnose, early_stopping_epoch


class TestEarlyStopping(unittest.TestCase):
    def test_stops_before_a_late_minimum(self):
        self.assertEqual(early_stopping_epoch([5, 4, 3, 3.5, 3.2, 3.1, 2.0], 3), 2)

    def test_patience_survives_a_blip(self):
        self.assertEqual(early_stopping_epoch([5, 4, 3, 3.5, 2.5, 2.4], 2), 5)
        # patience 1 stops at the first bad epoch
        self.assertEqual(early_stopping_epoch([5, 4, 3, 3.5, 2.5, 2.4], 1), 2)

    def test_equal_loss_is_not_an_improvement(self):
        self.assertEqual(early_stopping_epoch([3, 2, 2, 2], 5), 1)
        # the plateau uses up patience, so the later 1.0 is never reached
        self.assertEqual(early_stopping_epoch([3, 2, 2, 2, 1.0], 2), 1)
        self.assertEqual(early_stopping_epoch([3, 2, 2, 2, 1.0], 3), 4)

    def test_runs_out_of_data(self):
        self.assertEqual(early_stopping_epoch([4.0], 1), 0)
        self.assertEqual(early_stopping_epoch([4, 3, 2, 1], 2), 3)
        self.assertEqual(early_stopping_epoch([1, 2, 3], 10), 0)

    def test_long_curve(self):
        losses = [1.0 / (e + 1) for e in range(1000)] + [0.5] * 10 + [0.0]
        self.assertEqual(early_stopping_epoch(losses, 10), 999)
        self.assertEqual(early_stopping_epoch(losses, 11), 1010)

    def test_early_stopping_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            early_stopping_epoch([], 3)
        with self.assertRaises(ValueError):
            early_stopping_epoch([1.0, 2.0], 0)

    def test_diagnose_examples(self):
        self.assertEqual(diagnose([2.0, 1.5], [2.1, 1.6], 0.5, 0.2), "underfit")
        self.assertEqual(diagnose([1.0, 0.1], [1.1, 0.9], 0.5, 0.2), "overfit")
        self.assertEqual(diagnose([1.0, 0.3], [1.1, 0.4], 0.5, 0.2), "ok")

    def test_diagnose_uses_final_values_and_order(self):
        # early epochs look overfit, final epoch is fine
        self.assertEqual(diagnose([0.1, 0.2], [3.0, 0.3], 0.5, 0.2), "ok")
        # high train loss with a huge gap is still underfit first
        self.assertEqual(diagnose([2.0], [9.0], 0.5, 0.2), "underfit")
        # boundaries are not over the limit
        self.assertEqual(diagnose([0.5], [0.75], 0.5, 0.25), "ok")

    def test_diagnose_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            diagnose([], [], 0.5, 0.2)
        with self.assertRaises(ValueError):
            diagnose([1.0, 0.5], [1.0], 0.5, 0.2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
