import unittest

from solution import KthLargest


def add_all(tracker: KthLargest, values: list[int]) -> list[int | None]:
    return [tracker.add(v) for v in values]


class TestKthLargest(unittest.TestCase):
    def test_3rd_largest_as_numbers_arrive(self):
        self.assertEqual(add_all(KthLargest(3), [4, 5, 8, 2, 9, 4]), [None, None, 4, 4, 5, 5])

    def test_k_1_tracks_the_maximum(self):
        self.assertEqual(add_all(KthLargest(1), [3, 1, 7, 7]), [3, 3, 7, 7])

    def test_duplicates_count_separately(self):
        self.assertEqual(add_all(KthLargest(2), [5, 5, 5, 6, 6]), [None, 5, 5, 5, 6])

    def test_negative_numbers(self):
        self.assertEqual(add_all(KthLargest(2), [-1, -5, -3, 0]), [None, -5, -3, -1])

    def test_instances_keep_separate_numbers(self):
        a = KthLargest(2)
        b = KthLargest(1)
        self.assertIsNone(a.add(1))
        self.assertEqual(b.add(10), 10)
        self.assertEqual(a.add(2), 1)
        self.assertEqual(b.add(3), 10)

    def test_200000_additions_with_k_50000_log_k_each(self):
        tracker = KthLargest(50000)
        total = 0
        last = None
        for i in range(200000):
            last = tracker.add((i * 7919) % 200003)
            if last is not None:
                total += last
        self.assertEqual(last, 150000)
        self.assertEqual(total, 16136295473)


if __name__ == "__main__":
    unittest.main(verbosity=2)
