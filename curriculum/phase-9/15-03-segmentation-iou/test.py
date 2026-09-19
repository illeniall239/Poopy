import unittest

from solution import mean_iou

PRED = [[0, 0, 1], [0, 1, 1]]
TRUE = [[0, 0, 0], [0, 1, 1]]


class TestSegmentationIoU(unittest.TestCase):
    def assertPerClass(self, got, want):
        self.assertEqual(len(got), len(want))
        for g, w in zip(got, want):
            if w is None:
                self.assertIsNone(g)
            else:
                self.assertAlmostEqual(g, w, delta=1e-9)

    def test_two_classes_by_hand(self):
        per_class, mean = mean_iou(PRED, TRUE, 2)
        self.assertPerClass(per_class, [0.75, 2 / 3])
        self.assertAlmostEqual(mean, (0.75 + 2 / 3) / 2, delta=1e-9)

    def test_absent_class_is_none_and_ignored(self):
        per_class, mean = mean_iou(PRED, TRUE, 3)
        self.assertPerClass(per_class, [0.75, 2 / 3, None])
        self.assertAlmostEqual(mean, (0.75 + 2 / 3) / 2, delta=1e-9)

    def test_perfect_prediction(self):
        per_class, mean = mean_iou(TRUE, TRUE, 2)
        self.assertPerClass(per_class, [1.0, 1.0])
        self.assertAlmostEqual(mean, 1.0, delta=1e-9)

    def test_missed_class_counts_as_zero(self):
        true = [[0] * 10 for _ in range(10)]
        true[4][4] = true[4][5] = true[5][4] = true[5][5] = 1
        pred = [[0] * 10 for _ in range(10)]
        per_class, mean = mean_iou(pred, true, 2)
        self.assertPerClass(per_class, [0.96, 0.0])
        self.assertAlmostEqual(mean, 0.48, delta=1e-9)

    def test_class_only_in_prediction(self):
        per_class, mean = mean_iou([[2, 0], [0, 0]], [[0, 0], [0, 0]], 3)
        self.assertPerClass(per_class, [0.75, None, 0.0])
        self.assertAlmostEqual(mean, 0.375, delta=1e-9)

    def test_returns_float_mean(self):
        _, mean = mean_iou([[1]], [[1]], 2)
        self.assertIsInstance(mean, float)
        self.assertEqual(mean, 1.0)

    def test_errors(self):
        with self.assertRaises(ValueError):
            mean_iou([[0, 1]], [[0]], 2)
        with self.assertRaises(ValueError):
            mean_iou([[0], [1]], [[0]], 2)
        with self.assertRaises(ValueError):
            mean_iou([[0, 3]], [[0, 1]], 2)
        with self.assertRaises(ValueError):
            mean_iou([[0, -1]], [[0, 1]], 2)
        with self.assertRaises(ValueError):
            mean_iou([], [], 2)
        with self.assertRaises(ValueError):
            mean_iou([[0]], [[0]], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
