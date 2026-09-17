import unittest

from solution import triangle_kind


class TestTriangleKind(unittest.TestCase):
    def test_all_sides_equal_is_equilateral_not_isosceles(self):
        self.assertEqual(triangle_kind(3, 3, 3), "equilateral")

    def test_two_equal_sides_in_any_position_is_isosceles(self):
        self.assertEqual(triangle_kind(3, 3, 5), "isosceles")
        self.assertEqual(triangle_kind(5, 3, 3), "isosceles")
        self.assertEqual(triangle_kind(3, 5, 3), "isosceles")

    def test_no_equal_sides_is_scalene(self):
        self.assertEqual(triangle_kind(3, 4, 5), "scalene")
        self.assertEqual(triangle_kind(5, 3, 4), "scalene")

    def test_flat_triangle_is_invalid(self):
        self.assertEqual(triangle_kind(1, 2, 3), "invalid")
        self.assertEqual(triangle_kind(3, 1, 2), "invalid")

    def test_two_equal_sides_that_are_too_short_is_invalid_not_isosceles(self):
        self.assertEqual(triangle_kind(1, 1, 5), "invalid")
        self.assertEqual(triangle_kind(5, 1, 1), "invalid")

    def test_all_sides_zero_is_invalid_not_equilateral(self):
        self.assertEqual(triangle_kind(0, 0, 0), "invalid")

    def test_negative_sides_are_invalid(self):
        self.assertEqual(triangle_kind(-3, 4, 5), "invalid")
        self.assertEqual(triangle_kind(-2, -2, -2), "invalid")

    def test_just_valid_when_two_sides_add_up_to_one_more_than_the_third(self):
        self.assertEqual(triangle_kind(2, 3, 4), "scalene")
        self.assertEqual(triangle_kind(1, 1, 1), "equilateral")


if __name__ == "__main__":
    unittest.main(verbosity=2)
