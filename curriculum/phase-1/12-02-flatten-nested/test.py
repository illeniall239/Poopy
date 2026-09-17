import unittest

from solution import depth, flatten


class TestFlattenNested(unittest.TestCase):
    def test_flattens_mixed_nesting_in_left_to_right_order(self):
        self.assertEqual(flatten([1, [2, 3], [[4]], 5]), [1, 2, 3, 4, 5])

    def test_empty_lists_contribute_nothing(self):
        self.assertEqual(flatten([[], [[]], 6]), [6])
        self.assertEqual(flatten([]), [])

    def test_already_flat_input_comes_back_as_a_new_equal_list(self):
        input = [3, 1, 2]
        result = flatten(input)
        self.assertEqual(result, [3, 1, 2])
        self.assertIsNot(result, input)

    def test_handles_deep_nesting(self):
        deep = 42
        for _ in range(100):
            deep = [deep]
        self.assertEqual(flatten([0, deep, 1]), [0, 42, 1])

    def test_does_not_change_the_input(self):
        input = [1, [2, [3]], []]
        flatten(input)
        depth(input)
        self.assertEqual(input, [1, [2, [3]], []])

    def test_depth_of_flat_lists_is_1(self):
        self.assertEqual(depth([1, 2, 3]), 1)
        self.assertEqual(depth([]), 1)

    def test_depth_takes_the_deepest_branch(self):
        self.assertEqual(depth([1, [2, [3]], [4]]), 3)
        self.assertEqual(depth([[4], [2, [3]]]), 3)
        self.assertEqual(depth([[], 1]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
