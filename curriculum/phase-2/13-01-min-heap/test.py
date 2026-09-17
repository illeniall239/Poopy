import unittest

from solution import MinHeap


def drain(heap: MinHeap) -> list[int]:
    out = []
    while heap.size() > 0:
        out.append(heap.pop())
    return out


class TestMinHeap(unittest.TestCase):
    def test_empty_heap_has_size_0_and_returns_none(self):
        heap = MinHeap()
        self.assertEqual(heap.size(), 0)
        self.assertIsNone(heap.peek())
        self.assertIsNone(heap.pop())

    def test_peek_returns_the_smallest_without_removing_it(self):
        heap = MinHeap()
        for v in [5, 3, 8]:
            heap.push(v)
        self.assertEqual(heap.peek(), 3)
        self.assertEqual(heap.size(), 3)

    def test_pops_come_out_smallest_first_duplicates_included(self):
        heap = MinHeap()
        for v in [5, 3, 8, 3, 1, 9, 2]:
            heap.push(v)
        self.assertEqual(drain(heap), [1, 2, 3, 3, 5, 8, 9])
        self.assertIsNone(heap.pop())

    def test_negative_numbers(self):
        heap = MinHeap()
        for v in [0, -4, 7, -10, 2]:
            heap.push(v)
        self.assertEqual(drain(heap), [-10, -4, 0, 2, 7])

    def test_interleaved_push_and_pop(self):
        heap = MinHeap()
        heap.push(4)
        heap.push(7)
        self.assertEqual(heap.pop(), 4)
        heap.push(1)
        heap.push(6)
        self.assertEqual(heap.pop(), 1)
        self.assertEqual(heap.peek(), 6)
        self.assertEqual(heap.size(), 2)

    def test_builds_from_a_starting_list_without_changing_it(self):
        values = [9, 4, 7, 1, 8, 2]
        heap = MinHeap(values)
        self.assertEqual(heap.size(), 6)
        self.assertEqual(drain(heap), [1, 2, 4, 7, 8, 9])
        self.assertEqual(values, [9, 4, 7, 1, 8, 2])

    def test_100000_pushes_then_pops_log_n_each(self):
        n = 100000
        heap = MinHeap()
        values = []
        for i in range(n):
            v = (i * 7919) % 100003
            values.append(v)
            heap.push(v)
        self.assertEqual(drain(heap), sorted(values))


if __name__ == "__main__":
    unittest.main(verbosity=2)
