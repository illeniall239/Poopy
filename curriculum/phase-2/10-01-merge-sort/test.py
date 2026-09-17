import unittest

from solution import merge_sort


class TestMergeSort(unittest.TestCase):
    def test_sorts_a_small_list_with_a_duplicate(self):
        self.assertEqual(merge_sort([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9])

    def test_compares_as_numbers_not_as_strings(self):
        self.assertEqual(merge_sort([10, 9, 100, 1]), [1, 9, 10, 100])

    def test_negative_numbers_and_zero(self):
        self.assertEqual(merge_sort([-3, 0, -7, 4, -1000000000, 1000000000]), [-1000000000, -7, -3, 0, 4, 1000000000])

    def test_empty_and_single_element_lists(self):
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([42]), [42])

    def test_already_sorted_reversed_and_all_equal(self):
        self.assertEqual(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
        self.assertEqual(merge_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])
        self.assertEqual(merge_sort([7, 7, 7, 7]), [7, 7, 7, 7])

    def test_odd_length_where_one_half_has_leftovers(self):
        self.assertEqual(merge_sort([8, 1, 9, 2, 10, 3, 11]), [1, 2, 3, 8, 9, 10, 11])

    def test_returns_a_new_list_and_leaves_the_input_unchanged(self):
        nums = [3, 1, 2]
        result = merge_sort(nums)
        self.assertEqual(result, [1, 2, 3])
        self.assertEqual(nums, [3, 1, 2])
        self.assertIsNot(result, nums)

    def test_100000_shuffled_numbers_in_n_log_n(self):
        n = 100000
        nums = [((i * 7919 + 13) % 1000003) - 500000 for i in range(n)]
        self.assertEqual(merge_sort(nums), sorted(nums))


if __name__ == "__main__":
    unittest.main(verbosity=2)
