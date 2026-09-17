import unittest

from solution import second_largest


class TestSecondLargest(unittest.TestCase):
    def test_unsorted_distinct_values(self):
        self.assertEqual(second_largest([3, 1, 2]), 2)

    def test_duplicates_of_the_largest_are_skipped(self):
        self.assertEqual(second_largest([5, 5, 4]), 4)

    def test_all_negative_numbers(self):
        self.assertEqual(second_largest([-1, -3, -2]), -2)

    def test_all_values_equal_gives_none(self):
        self.assertIsNone(second_largest([7, 7, 7]))

    def test_empty_and_single_element_lists_give_none(self):
        self.assertIsNone(second_largest([]))
        self.assertIsNone(second_largest([9]))

    def test_new_largest_pushes_old_largest_into_second_place(self):
        self.assertEqual(second_largest([1, 2, 3, 10]), 3)

    def test_second_largest_appears_after_the_largest(self):
        self.assertEqual(second_largest([10, 1, 8, 10, 8]), 8)

    def test_zero_can_be_the_answer(self):
        self.assertEqual(second_largest([0, -4, 6]), 0)

    def test_does_not_modify_the_input(self):
        nums = [4, 9, 2, 9]
        second_largest(nums)
        self.assertEqual(nums, [4, 9, 2, 9])


if __name__ == "__main__":
    unittest.main(verbosity=2)
