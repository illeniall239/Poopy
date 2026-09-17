import unittest

from solution import top_k_frequent


class TestTopKFrequent(unittest.TestCase):
    def test_most_frequent_first(self):
        self.assertEqual(top_k_frequent([1, 1, 1, 2, 2, 3], 2), [1, 2])

    def test_k_1_gives_the_single_most_frequent_value(self):
        self.assertEqual(top_k_frequent([4, 5, 5, 6], 1), [5])

    def test_ties_go_to_the_value_that_appears_first(self):
        self.assertEqual(top_k_frequent([9, 4, 4, 9, 1], 2), [9, 4])
        self.assertEqual(top_k_frequent([4, 9, 9, 4, 1], 2), [4, 9])

    def test_frequency_beats_first_appearance(self):
        self.assertEqual(top_k_frequent([3, 1, 1, 3, 2, 2, 2], 3), [2, 3, 1])

    def test_all_distinct_values_keep_their_order(self):
        self.assertEqual(top_k_frequent([5, 3, 8, 1], 3), [5, 3, 8])

    def test_negative_values_and_zero(self):
        self.assertEqual(top_k_frequent([-1, -1, 0, 0, 0, 2], 2), [0, -1])

    def test_k_equal_to_the_number_of_distinct_values(self):
        self.assertEqual(top_k_frequent([7, 8, 8, 9, 9, 9], 3), [9, 8, 7])

    def test_does_not_change_the_input(self):
        values = [2, 1, 2]
        top_k_frequent(values, 1)
        self.assertEqual(values, [2, 1, 2])

    def test_60000_values_with_20000_distinct_in_o_n(self):
        values = [i % 20000 for i in range(60000)]
        values += [12345, 777, 12345, 777, 12345]
        self.assertEqual(top_k_frequent(values, 3), [12345, 777, 0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
