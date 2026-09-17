import math
import unittest

from solution import Circle, Rectangle, Triangle, area


class TestArea(unittest.TestCase):
    def test_unit_circle(self):
        self.assertEqual(area(Circle(radius=1)), math.pi)

    def test_circle_area_grows_with_the_square_of_the_radius(self):
        self.assertEqual(area(Circle(radius=2)), 4 * math.pi)
        self.assertEqual(area(Circle(radius=0.5)), math.pi / 4)

    def test_rectangle(self):
        self.assertEqual(area(Rectangle(width=3, height=4)), 12)

    def test_triangle_is_half_of_base_times_height(self):
        self.assertEqual(area(Triangle(base=5, height=3)), 7.5)

    def test_rectangle_and_triangle_with_the_same_numbers_differ(self):
        self.assertEqual(area(Rectangle(width=4, height=5)), 20)
        self.assertEqual(area(Triangle(base=4, height=5)), 10)

    def test_zero_sized_shapes_have_zero_area(self):
        self.assertEqual(area(Circle(radius=0)), 0)
        self.assertEqual(area(Rectangle(width=0, height=9)), 0)
        self.assertEqual(area(Triangle(base=7, height=0)), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
