import unittest

from solution import climb_ways


class TestClimbWays(unittest.TestCase):
    def test_zero_steps_one_way(self):
        self.assertEqual(climb_ways(0), 1)

    def test_one_step(self):
        self.assertEqual(climb_ways(1), 1)

    def test_two_steps(self):
        self.assertEqual(climb_ways(2), 2)

    def test_three_steps(self):
        self.assertEqual(climb_ways(3), 3)

    def test_five_steps(self):
        self.assertEqual(climb_ways(5), 8)

    def test_ten_steps(self):
        self.assertEqual(climb_ways(10), 89)

    def test_45_steps_needs_stored_sub_answers(self):
        self.assertEqual(climb_ways(45), 1836311903)

    def test_70_steps(self):
        self.assertEqual(climb_ways(70), 308061521170129)


if __name__ == "__main__":
    unittest.main(verbosity=2)
