import unittest

from solution import max_and_min


class TestMaxAndMin(unittest.TestCase):
    def test_mixed_positive_numbers(self):
        self.assertEqual(max_and_min([3, 9, 1, 4]), {"max": 9, "min": 1})

    def test_all_negative_numbers_max_is_not_0(self):
        self.assertEqual(max_and_min([-5, -2, -8]), {"max": -2, "min": -8})

    def test_all_positive_numbers_min_is_not_0(self):
        self.assertEqual(max_and_min([12, 40, 7, 30]), {"max": 40, "min": 7})

    def test_single_element_is_both_max_and_min(self):
        self.assertEqual(max_and_min([7]), {"max": 7, "min": 7})

    def test_empty_list_returns_none(self):
        self.assertIsNone(max_and_min([]))

    def test_max_first_and_min_last(self):
        self.assertEqual(max_and_min([100, 50, 0, -50]), {"max": 100, "min": -50})

    def test_decimals_and_repeated_values(self):
        self.assertEqual(max_and_min([2.5, 2.5, -0.5, 2.5]), {"max": 2.5, "min": -0.5})

    def test_does_not_modify_the_input(self):
        nums = [4, 1, 3]
        max_and_min(nums)
        self.assertEqual(nums, [4, 1, 3])


if __name__ == "__main__":
    unittest.main(verbosity=2)
