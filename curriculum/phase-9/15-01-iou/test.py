import unittest

from solution import iou


class TestIoU(unittest.TestCase):
    def test_identical_boxes(self):
        self.assertAlmostEqual(iou([0, 0, 2, 2], [0, 0, 2, 2]), 1.0, delta=1e-9)

    def test_partial_overlap_subtracts_the_intersection_once(self):
        self.assertAlmostEqual(iou([0, 0, 2, 2], [1, 1, 3, 3]), 1 / 7, delta=1e-9)
        self.assertAlmostEqual(iou([0, 0, 4, 2], [2, 0, 6, 2]), 4 / 12, delta=1e-9)

    def test_contained_box(self):
        self.assertAlmostEqual(iou([0, 0, 4, 4], [1, 1, 3, 3]), 0.25, delta=1e-9)
        self.assertAlmostEqual(iou([1, 1, 3, 3], [0, 0, 4, 4]), 0.25, delta=1e-9)

    def test_disjoint_and_touching_are_zero(self):
        self.assertEqual(iou([0, 0, 1, 1], [2, 2, 3, 3]), 0.0)
        self.assertEqual(iou([0, 0, 1, 1], [1, 0, 2, 1]), 0.0)
        self.assertEqual(iou([0, 0, 1, 1], [1, 1, 2, 2]), 0.0)
        # overlapping in x only: the negative height must not make a positive product
        self.assertEqual(iou([0, 0, 2, 1], [1, 3, 3, 4]), 0.0)
        self.assertEqual(iou([0, 3, 2, 4], [1, 0, 3, 1]), 0.0)

    def test_float_coordinates_and_symmetry(self):
        a, b = [0.5, 0.25, 2.5, 1.75], [1.0, 1.0, 3.0, 2.0]
        # intersection 1.5 x 0.75, areas 3.0 and 2.0
        want = 1.125 / (3.0 + 2.0 - 1.125)
        self.assertAlmostEqual(iou(a, b), want, delta=1e-9)
        self.assertAlmostEqual(iou(b, a), want, delta=1e-9)

    def test_returns_float(self):
        self.assertIsInstance(iou([0, 0, 2, 2], [0, 0, 2, 2]), float)
        self.assertIsInstance(iou([0, 0, 1, 1], [5, 5, 6, 6]), float)

    def test_rejects_invalid_boxes(self):
        for a, b in [([0, 0, 1, 1], [1, 1, 0, 2]), ([0, 0, 0, 1], [0, 0, 1, 1]), ([0, 0, 1], [0, 0, 1, 1])]:
            with self.assertRaises(ValueError, msg=f"{a} {b}"):
                iou(a, b)


if __name__ == "__main__":
    unittest.main(verbosity=2)
