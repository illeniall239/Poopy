import unittest

from solution import max_sum_fixed_window


class TestMaxSumFixedWindow(unittest.TestCase):
    def test_best_window_in_the_middle(self):
        self.assertEqual(max_sum_fixed_window([2, 1, 5, 1, 3, 2], 3), 9)

    def test_best_window_at_the_end(self):
        self.assertEqual(max_sum_fixed_window([2, 3, 4, 1, 5], 2), 7)
        self.assertEqual(max_sum_fixed_window([4, -1, 2, -7, 5, 6], 1), 6)

    def test_all_negative_values_give_a_negative_sum(self):
        self.assertEqual(max_sum_fixed_window([-1, -2, -3, -4], 2), -3)

    def test_window_covers_the_whole_list(self):
        self.assertEqual(max_sum_fixed_window([1, 2, 3], 3), 6)
        self.assertEqual(max_sum_fixed_window([5], 1), 5)

    def test_k_larger_than_the_list_gives_0(self):
        self.assertEqual(max_sum_fixed_window([1, 2], 3), 0)
        self.assertEqual(max_sum_fixed_window([], 1), 0)

    def test_all_windows_equal(self):
        self.assertEqual(max_sum_fixed_window([3, 3, 3, 3], 2), 6)

    def test_does_not_change_the_input(self):
        values = [1, 2, 3]
        max_sum_fixed_window(values, 2)
        self.assertEqual(values, [1, 2, 3])

    def test_60000_values_with_a_window_of_20500_in_o_n(self):
        n = 60000
        values = [i % 1000 for i in range(n)]
        self.assertEqual(max_sum_fixed_window(values, 20500), 20 * 499500 + 374750)


if __name__ == "__main__":
    unittest.main(verbosity=2)
