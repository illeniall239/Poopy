import unittest

from solution import TwoStackQueue


class TestTwoStackQueue(unittest.TestCase):
    def test_values_come_out_in_the_order_they_went_in(self):
        q = TwoStackQueue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual([q.dequeue(), q.dequeue(), q.dequeue()], [1, 2, 3])

    def test_peek_returns_the_front_without_removing_it(self):
        q = TwoStackQueue()
        q.enqueue("a")
        q.enqueue("b")
        self.assertEqual([q.peek(), q.peek(), q.size(), q.dequeue()], ["a", "a", 2, "a"])

    def test_mixed_enqueues_and_dequeues_keep_fifo_order(self):
        q = TwoStackQueue()
        q.enqueue(1)
        q.enqueue(2)
        first = q.dequeue()
        q.enqueue(3)
        q.enqueue(4)
        second = q.dequeue()
        q.enqueue(5)
        self.assertEqual([first, second, q.dequeue(), q.dequeue(), q.dequeue()], [1, 2, 3, 4, 5])

    def test_empty_queue_returns_none_and_size_0(self):
        q = TwoStackQueue()
        self.assertEqual([q.size(), q.dequeue(), q.peek(), q.size()], [0, None, None, 0])

    def test_size_counts_values_on_both_sides(self):
        q = TwoStackQueue()
        q.enqueue(1)
        q.enqueue(2)
        q.dequeue()
        q.enqueue(3)
        q.enqueue(4)
        self.assertEqual(q.size(), 3)

    def test_dequeue_on_an_empty_queue_changes_nothing(self):
        q = TwoStackQueue()
        q.dequeue()
        q.enqueue(7)
        self.assertEqual([q.size(), q.dequeue(), q.size()], [1, 7, 0])

    def test_separate_queues_do_not_share_values(self):
        a = TwoStackQueue()
        b = TwoStackQueue()
        a.enqueue(1)
        b.enqueue(2)
        self.assertEqual([a.dequeue(), b.dequeue(), a.size(), b.size()], [1, 2, 0, 0])

    def test_200000_values_with_200000_mixed_calls_amortized_constant(self):
        n = 200000
        q = TwoStackQueue()
        for i in range(n):
            q.enqueue(i)
        wrong = 0
        for i in range(n):
            if q.peek() != i:
                wrong += 1
            if q.dequeue() != i:
                wrong += 1
            q.enqueue(n + i)
        self.assertEqual(wrong, 0)
        self.assertEqual(q.size(), n)
        self.assertEqual(q.peek(), n)


if __name__ == "__main__":
    unittest.main(verbosity=2)
