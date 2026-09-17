import unittest

from solution import can_reach_last_index


class TestCanReachLastIndex(unittest.TestCase):
    def test_reachable_with_a_choice_of_routes(self):
        self.assertTrue(can_reach_last_index([2, 3, 1, 1, 4]))

    def test_every_route_lands_on_a_zero(self):
        self.assertFalse(can_reach_last_index([3, 2, 1, 0, 4]))

    def test_single_square(self):
        self.assertTrue(can_reach_last_index([0]))

    def test_two_squares(self):
        self.assertFalse(can_reach_last_index([0, 1]))
        self.assertTrue(can_reach_last_index([1, 0]))

    def test_landing_exactly_on_the_last_square(self):
        self.assertTrue(can_reach_last_index([2, 0, 0]))

    def test_jumping_past_the_end_counts_as_reaching_it(self):
        self.assertTrue(can_reach_last_index([10, 0, 0]))

    def test_stuck_before_the_end_despite_a_later_non_zero(self):
        self.assertFalse(can_reach_last_index([4, 1, 1, 0, 0, 1]))

    def test_100000_squares_reachable_in_linear_time(self):
        n = 100000
        self.assertTrue(can_reach_last_index([n - 1 - i for i in range(n)]))

    def test_100000_squares_unreachable_in_linear_time(self):
        n = 100000
        self.assertFalse(can_reach_last_index([max(0, n - 2 - i) for i in range(n)]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
