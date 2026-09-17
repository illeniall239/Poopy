import unittest

from solution import average


class TestAverage(unittest.TestCase):
    def test_empty_list_gives_none(self):
        self.assertIsNone(average([]))

    def test_all_zeros_average_to_0(self):
        self.assertEqual(average([0, 0, 0]), 0)

    def test_single_value_is_its_own_average(self):
        self.assertEqual(average([5]), 5)

    def test_whole_number_average(self):
        self.assertEqual(average([2, 4, 6]), 4)

    def test_average_is_not_rounded(self):
        self.assertEqual(average([1, 2]), 1.5)
        self.assertEqual(average([1, 1, 2]), 4 / 3)

    def test_negative_numbers(self):
        self.assertEqual(average([-1, -2]), -1.5)

    def test_first_element_counts(self):
        self.assertEqual(average([100, 0, 0, 0]), 25)


if __name__ == "__main__":
    unittest.main(verbosity=2)
