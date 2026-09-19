import unittest

from solution import iou, nms

BOXES = [[0, 0, 10, 10], [1, 1, 11, 11], [20, 20, 30, 30], [0, 0, 9, 10]]
SCORES = [0.9, 0.8, 0.7, 0.95]


class TestNMS(unittest.TestCase):
    def test_iou_helper(self):
        self.assertAlmostEqual(iou([0, 0, 2, 2], [1, 1, 3, 3]), 1 / 7, delta=1e-9)
        self.assertEqual(iou([0, 0, 1, 1], [1, 0, 2, 1]), 0.0)
        self.assertEqual(iou([0, 0, 2, 1], [1, 3, 3, 4]), 0.0)

    def test_keeps_highest_scores_first(self):
        self.assertEqual(nms(BOXES, SCORES, 0.5), [3, 2])

    def test_high_threshold_keeps_everything_in_score_order(self):
        self.assertEqual(nms(BOXES, SCORES, 0.95), [3, 0, 1, 2])

    def test_only_kept_boxes_suppress(self):
        # A overlaps B, B overlaps C, A and C are disjoint: B is suppressed, so C survives.
        boxes = [[0, 0, 10, 10], [5, 0, 15, 10], [10, 0, 20, 10]]
        self.assertEqual(nms(boxes, [0.9, 0.8, 0.7], 0.3), [0, 2])

    def test_suppression_needs_strictly_greater_iou(self):
        boxes = [[0, 0, 2, 1], [0, 0, 1, 1]]  # IoU exactly 0.5
        self.assertEqual(nms(boxes, [0.6, 0.9], 0.5), [1, 0])
        self.assertEqual(nms(boxes, [0.6, 0.9], 0.49), [1])

    def test_equal_scores_keep_lower_index_first(self):
        boxes = [[0, 0, 10, 10], [0, 0, 10, 9], [50, 50, 60, 60]]
        self.assertEqual(nms(boxes, [0.5, 0.5, 0.5], 0.5), [0, 2])

    def test_per_class_suppression(self):
        self.assertEqual(nms(BOXES, SCORES, 0.5, labels=[0, 1, 0, 0]), [3, 1, 2])
        self.assertEqual(nms(BOXES, SCORES, 0.5, labels=[0, 1, 2, 3]), [3, 0, 1, 2])

    def test_empty_and_errors(self):
        self.assertEqual(nms([], [], 0.5), [])
        with self.assertRaises(ValueError):
            nms([[0, 0, 1, 1]], [0.5, 0.4], 0.5)
        with self.assertRaises(ValueError):
            nms([[0, 0, 1, 1]], [0.5], 0.5, labels=[0, 1])
        with self.assertRaises(ValueError):
            nms([[0, 0, 1, 1]], [0.5], 1.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
