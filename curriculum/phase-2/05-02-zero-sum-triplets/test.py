import unittest

from solution import zero_sum_triplets


class TestZeroSumTriplets(unittest.TestCase):
    def test_two_triplets_in_lexicographic_order(self):
        self.assertEqual(zero_sum_triplets([-1, 0, 1, 2, -1, -4]), [[-1, -1, 2], [-1, 0, 1]])

    def test_all_zeros_give_one_triplet(self):
        self.assertEqual(zero_sum_triplets([0, 0, 0]), [[0, 0, 0]])
        self.assertEqual(zero_sum_triplets([0, 0, 0, 0]), [[0, 0, 0]])

    def test_a_repeated_value_may_be_used_twice_in_one_triplet(self):
        self.assertEqual(zero_sum_triplets([-2, 0, 1, 1, 2]), [[-2, 0, 2], [-2, 1, 1]])

    def test_duplicates_of_the_first_value_do_not_repeat_a_triplet(self):
        self.assertEqual(zero_sum_triplets([3, -1, -2, -2, 4, -1, 0]), [[-2, -2, 4], [-2, -1, 3]])

    def test_no_triplet_gives_an_empty_list(self):
        self.assertEqual(zero_sum_triplets([1, 2, -2, -1]), [])
        self.assertEqual(zero_sum_triplets([1, 2, 3]), [])

    def test_fewer_than_three_values_give_an_empty_list(self):
        self.assertEqual(zero_sum_triplets([]), [])
        self.assertEqual(zero_sum_triplets([0]), [])
        self.assertEqual(zero_sum_triplets([1, -1]), [])

    def test_does_not_change_the_input(self):
        values = [2, -1, -1, 0]
        zero_sum_triplets(values)
        self.assertEqual(values, [2, -1, -1, 0])

    def test_800_values_with_two_triplets_in_o_n_squared(self):
        n = 800
        values = list(range(1, n - 1)) + [-3, -2]
        self.assertEqual(zero_sum_triplets(values), [[-3, -2, 5], [-3, 1, 2]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
