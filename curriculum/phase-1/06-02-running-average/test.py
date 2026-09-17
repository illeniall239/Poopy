import unittest

from solution import running_averages


class TestRunningAverages(unittest.TestCase):
    def test_increasing_numbers(self):
        self.assertEqual(running_averages([1, 2, 3, 4]), [1, 1.5, 2, 2.5])

    def test_negative_numbers_pull_the_average_down(self):
        self.assertEqual(running_averages([10, -10, 6]), [10, 0, 2])

    def test_single_element(self):
        self.assertEqual(running_averages([5]), [5])

    def test_empty_list_gives_empty_list(self):
        self.assertEqual(running_averages([]), [])

    def test_constant_values_keep_a_constant_average(self):
        self.assertEqual(running_averages([4, 4, 4, 4]), [4, 4, 4, 4])

    def test_first_element_is_its_own_average_divide_by_count_so_far(self):
        self.assertEqual(running_averages([8, 0, 0, 0]), [8, 4, 8 / 3, 2])

    def test_does_not_modify_the_input(self):
        nums = [3, 5, 7]
        result = running_averages(nums)
        self.assertEqual(nums, [3, 5, 7])
        self.assertIsNot(result, nums)

    def test_large_input(self):
        nums = [2] * 100000
        result = running_averages(nums)
        self.assertEqual(len(result), 100000)
        self.assertEqual(result[99999], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
