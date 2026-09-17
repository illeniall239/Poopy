import unittest

from solution import chunk, last


class TestLastAndChunk(unittest.TestCase):
    def test_last_returns_the_final_element(self):
        self.assertEqual(last([3, 1, 4]), 4)
        self.assertEqual(last(["a"]), "a")

    def test_last_of_an_empty_list_is_none(self):
        self.assertIsNone(last([]))

    def test_last_returns_a_falsy_final_element_not_none(self):
        self.assertEqual(last([1, 0]), 0)
        self.assertIsNotNone(last([1, 0]))

    def test_chunk_leaves_a_shorter_final_group(self):
        self.assertEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])

    def test_chunk_with_size_equal_to_length_gives_one_group(self):
        self.assertEqual(chunk(["a", "b", "c"], 3), [["a", "b", "c"]])

    def test_chunk_with_size_larger_than_length_gives_one_group(self):
        self.assertEqual(chunk([1, 2], 10), [[1, 2]])

    def test_chunk_of_an_empty_list_is_empty(self):
        self.assertEqual(chunk([], 4), [])

    def test_chunk_rejects_sizes_below_1_or_not_whole(self):
        with self.assertRaises(ValueError):
            chunk([1, 2], 0)
        with self.assertRaises(ValueError):
            chunk([1, 2], -1)
        with self.assertRaises(ValueError):
            chunk([1, 2], 1.5)

    def test_neither_function_changes_the_input(self):
        items = [1, 2, 3]
        last(items)
        chunk(items, 2)
        self.assertEqual(items, [1, 2, 3])


if __name__ == "__main__":
    unittest.main(verbosity=2)
