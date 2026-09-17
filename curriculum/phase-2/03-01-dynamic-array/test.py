import unittest

from solution import DynamicArray


class TestDynamicArray(unittest.TestCase):
    def test_starts_empty_with_capacity_1(self):
        a = DynamicArray()
        self.assertEqual(a.size(), 0)
        self.assertEqual(a.capacity(), 1)
        self.assertEqual(a.to_list(), [])

    def test_push_then_get_keeps_order(self):
        a = DynamicArray()
        a.push("x")
        a.push("y")
        a.push("z")
        self.assertEqual(a.size(), 3)
        self.assertEqual([a.get(0), a.get(1), a.get(2)], ["x", "y", "z"])

    def test_capacity_doubles_only_when_full(self):
        a = DynamicArray()
        capacities = []
        for i in range(5):
            a.push(i)
            capacities.append(a.capacity())
        self.assertEqual(capacities, [1, 2, 4, 4, 8])

    def test_get_and_set_raise_index_error_outside_0_to_size_minus_1_even_below_capacity(self):
        a = DynamicArray()
        for v in [1, 2, 3]:
            a.push(v)
        self.assertEqual(a.capacity(), 4)
        with self.assertRaises(IndexError):
            a.get(3)
        with self.assertRaises(IndexError):
            a.get(-1)
        with self.assertRaises(IndexError):
            a.set(3, 9)

    def test_set_replaces_a_value_without_changing_the_size(self):
        a = DynamicArray()
        a.push(1)
        a.push(2)
        a.set(0, 7)
        self.assertEqual(a.to_list(), [7, 2])
        self.assertEqual(a.size(), 2)

    def test_pop_returns_the_last_element_and_never_shrinks_capacity(self):
        a = DynamicArray()
        for v in [1, 2, 3]:
            a.push(v)
        self.assertEqual(a.pop(), 3)
        self.assertEqual(a.pop(), 2)
        self.assertEqual(a.size(), 1)
        self.assertEqual(a.capacity(), 4)
        with self.assertRaises(IndexError):
            a.get(1)
        self.assertEqual(a.pop(), 1)
        with self.assertRaises(IndexError):
            a.pop()

    def test_to_list_returns_a_copy_that_cannot_break_the_structure(self):
        a = DynamicArray()
        for v in [1, 2, 3]:
            a.push(v)
        copy = a.to_list()
        self.assertEqual(len(copy), 3)
        copy[0] = 99
        copy.append(100)
        self.assertEqual(a.to_list(), [1, 2, 3])
        self.assertEqual(a.size(), 3)

    def test_200000_pushes_with_amortized_o_1_push(self):
        a = DynamicArray()
        n = 200000
        for i in range(n):
            a.push(i)
        self.assertEqual(a.size(), n)
        self.assertEqual(a.capacity(), 262144)
        self.assertEqual(a.get(n - 1), n - 1)
        self.assertEqual(a.get(123456), 123456)


if __name__ == "__main__":
    unittest.main(verbosity=2)
