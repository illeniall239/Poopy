import unittest

from solution import sorted_pair_sum


class TestSortedPairSum(unittest.TestCase):
    def test_finds_a_pair_in_the_middle(self):
        self.assertEqual(sorted_pair_sum([1, 2, 3, 4, 6], 6), [2, 4])

    def test_smallest_first_value_wins(self):
        self.assertEqual(sorted_pair_sum([1, 2, 3, 4], 5), [1, 4])
        self.assertEqual(sorted_pair_sum([0, 1, 2, 3, 4, 5], 5), [0, 5])

    def test_a_position_cannot_be_used_twice(self):
        self.assertEqual(sorted_pair_sum([2, 3, 4], 6), [2, 4])
        self.assertIsNone(sorted_pair_sum([1, 3, 7], 6))

    def test_equal_values_at_two_positions_form_a_pair(self):
        self.assertEqual(sorted_pair_sum([3, 3], 6), [3, 3])
        self.assertEqual(sorted_pair_sum([1, 4, 4, 9], 8), [4, 4])

    def test_negative_values_and_zero(self):
        self.assertEqual(sorted_pair_sum([-5, -2, 0, 4, 9], 2), [-2, 4])
        self.assertEqual(sorted_pair_sum([-3, 0, 0, 3], 0), [-3, 3])

    def test_no_pair_gives_none(self):
        self.assertIsNone(sorted_pair_sum([1, 2, 3], 100))
        self.assertIsNone(sorted_pair_sum([], 0))
        self.assertIsNone(sorted_pair_sum([7], 14))

    def test_does_not_change_the_input(self):
        values = [1, 2, 3]
        sorted_pair_sum(values, 4)
        self.assertEqual(values, [1, 2, 3])

    def test_extreme_values(self):
        self.assertEqual(sorted_pair_sum([-1000000000, 0, 1000000000], 0), [-1000000000, 1000000000])

    def test_30000_even_values_with_an_odd_target_in_o_n(self):
        n = 30000
        values = [2 * i for i in range(n)]
        self.assertIsNone(sorted_pair_sum(values, 2 * n - 3))


if __name__ == "__main__":
    unittest.main(verbosity=2)
