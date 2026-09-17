import unittest

from solution import rotate_right


class TestRotateRight(unittest.TestCase):
    def rotated(self, values, k):
        self.assertIsNone(rotate_right(values, k))
        return values

    def test_rotates_the_given_list_by_3(self):
        self.assertEqual(self.rotated([1, 2, 3, 4, 5, 6, 7], 3), [5, 6, 7, 1, 2, 3, 4])

    def test_k_0_leaves_the_list_alone(self):
        self.assertEqual(self.rotated([1, 2, 3], 0), [1, 2, 3])

    def test_k_equal_to_the_length_is_a_full_turn(self):
        self.assertEqual(self.rotated([1, 2, 3, 4], 4), [1, 2, 3, 4])

    def test_k_larger_than_the_length_wraps_around(self):
        self.assertEqual(self.rotated([1, 2, 3], 10), [3, 1, 2])

    def test_empty_list_stays_empty(self):
        self.assertEqual(self.rotated([], 5), [])

    def test_single_element(self):
        self.assertEqual(self.rotated([9], 4), [9])

    def test_duplicates_and_negative_values(self):
        self.assertEqual(self.rotated([-1, -1, 2, 0], 1), [0, -1, -1, 2])

    def test_400000_elements_with_a_huge_k_in_o_n(self):
        n = 400000
        values = list(range(n))
        rotate_right(values, 1000000000 + 200000)
        self.assertEqual(len(values), n)
        self.assertTrue(values == [(i + 200000) % n for i in range(n)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
