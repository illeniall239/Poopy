import unittest

from solution import quick_sort

N = 50000


def sorted_in_place(nums):
    quick_sort(nums)
    return nums


class TestQuickSort(unittest.TestCase):
    def test_sorts_a_small_list_with_a_duplicate(self):
        self.assertEqual(sorted_in_place([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9])

    def test_compares_as_numbers_with_negatives(self):
        self.assertEqual(sorted_in_place([10, -3, 9, 100, 0, -1000000000, 1]), [-1000000000, -3, 0, 1, 9, 10, 100])

    def test_empty_single_and_two_element_lists(self):
        self.assertEqual(sorted_in_place([]), [])
        self.assertEqual(sorted_in_place([42]), [42])
        self.assertEqual(sorted_in_place([2, 1]), [1, 2])

    def test_sorts_the_same_list_in_place_and_returns_nothing(self):
        nums = [3, 1, 2]
        self.assertIsNone(quick_sort(nums))
        self.assertEqual(nums, [1, 2, 3])

    def test_many_repeated_values(self):
        self.assertEqual(sorted_in_place([2, 1, 2, 3, 1, 2, 3, 1, 2]), [1, 1, 1, 2, 2, 2, 2, 3, 3])

    def test_50000_shuffled_numbers(self):
        nums = [((i * 7919 + 13) % 1000003) - 500000 for i in range(N)]
        expected = sorted(nums)
        quick_sort(nums)
        self.assertEqual(nums, expected)

    def test_50000_numbers_already_sorted_and_reversed(self):
        up = list(range(N))
        down = list(range(N, 0, -1))
        quick_sort(up)
        quick_sort(down)
        self.assertEqual(up, list(range(N)))
        self.assertEqual(down, list(range(1, N + 1)))

    def test_50000_equal_values(self):
        same = [7] * N
        quick_sort(same)
        self.assertEqual(same, [7] * N)

    def test_50000_values_drawn_from_only_three_numbers(self):
        few = [(i * 7) % 3 for i in range(N)]
        quick_sort(few)
        self.assertEqual(few, [0] * 16667 + [1] * 16667 + [2] * 16666)


if __name__ == "__main__":
    unittest.main(verbosity=2)
