import unittest

from solution import pair_with_target_sum


class TestPairWithTargetSum(unittest.TestCase):
    def test_finds_a_simple_pair(self):
        self.assertEqual(pair_with_target_sum([2, 7, 11, 15], 9), [0, 1])

    def test_an_element_does_not_pair_with_itself(self):
        self.assertEqual(pair_with_target_sum([3, 2, 4], 6), [1, 2])

    def test_equal_values_at_two_positions_form_a_pair(self):
        self.assertEqual(pair_with_target_sum([3, 3], 6), [0, 1])

    def test_smallest_j_wins_then_smallest_i(self):
        self.assertEqual(pair_with_target_sum([1, 3, 2, 4, 3], 6), [2, 3])
        self.assertEqual(pair_with_target_sum([2, 2, 4], 6), [0, 2])
        self.assertEqual(pair_with_target_sum([1, 5, 1, 5], 6), [0, 1])

    def test_no_pair_gives_minus_1_minus_1(self):
        self.assertEqual(pair_with_target_sum([5], 10), [-1, -1])
        self.assertEqual(pair_with_target_sum([], 0), [-1, -1])
        self.assertEqual(pair_with_target_sum([1, 2, 3], 100), [-1, -1])

    def test_negative_values_and_zero(self):
        self.assertEqual(pair_with_target_sum([-3, 4, 0, 3, 90], 0), [0, 3])
        self.assertEqual(pair_with_target_sum([0, 7, 0], 0), [0, 2])

    def test_does_not_change_the_input(self):
        values = [4, 1, 3]
        pair_with_target_sum(values, 4)
        self.assertEqual(values, [4, 1, 3])

    def test_extreme_values(self):
        self.assertEqual(pair_with_target_sum([-1000000000, 1000000000, -1000000000], -2000000000), [0, 2])

    def test_30000_values_with_the_only_pair_at_the_end_in_o_n(self):
        n = 30000
        values = list(range(n))
        self.assertEqual(pair_with_target_sum(values, 2 * n - 3), [n - 2, n - 1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
