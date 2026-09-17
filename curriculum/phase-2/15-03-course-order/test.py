import unittest

from solution import course_order


class TestCourseOrder(unittest.TestCase):
    def assert_valid_order(self, num_courses: int, prerequisites: list[list[int]], order: list[int]) -> None:
        """A valid order has every course exactly once and each required course before the course needing it."""
        self.assertEqual(len(order), num_courses, "order must contain every course")
        self.assertEqual(sorted(order), list(range(num_courses)), "each course exactly once")
        position = {course: i for i, course in enumerate(order)}
        for course, required in prerequisites:
            self.assertLess(position[required], position[course], f"{required} must come before {course}")

    def test_one_prerequisite(self):
        pre = [[1, 0]]
        self.assert_valid_order(2, pre, course_order(2, pre))

    def test_two_paths_to_the_same_course(self):
        pre = [[1, 0], [2, 0], [3, 1], [3, 2]]
        self.assert_valid_order(4, pre, course_order(4, pre))

    def test_no_prerequisites(self):
        self.assert_valid_order(3, [], course_order(3, []))

    def test_single_course(self):
        self.assertEqual(course_order(1, []), [0])

    def test_two_courses_requiring_each_other(self):
        self.assertEqual(course_order(2, [[0, 1], [1, 0]]), [])

    def test_cycle_that_does_not_include_every_course(self):
        self.assertEqual(course_order(4, [[1, 0], [2, 1], [3, 2], [1, 3]]), [])

    def test_repeated_pair(self):
        pre = [[1, 0], [1, 0], [2, 1]]
        self.assert_valid_order(3, pre, course_order(3, pre))

    def test_chain_of_100000_courses_in_linear_time(self):
        n = 100000
        pre = [[i, i + 1] for i in range(n - 1)]
        self.assert_valid_order(n, pre, course_order(n, pre))


if __name__ == "__main__":
    unittest.main(verbosity=2)
