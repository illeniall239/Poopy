import unittest

import numpy as np

from solution import minibatches


class TestMinibatches(unittest.TestCase):
    def test_every_index_exactly_once(self):
        for n, b in [(10, 4), (12, 4), (1, 1), (7, 7), (100, 3), (1000, 64)]:
            batches = list(minibatches(n, b, np.random.default_rng(n)))
            flat = [i for batch in batches for i in batch]
            self.assertEqual(sorted(flat), list(range(n)), (n, b))

    def test_batch_sizes_and_short_last_batch(self):
        batches = list(minibatches(10, 4, np.random.default_rng(0)))
        self.assertEqual([len(batch) for batch in batches], [4, 4, 2])
        batches = list(minibatches(12, 4, np.random.default_rng(0)))
        self.assertEqual([len(batch) for batch in batches], [4, 4, 4])
        batches = list(minibatches(3, 10, np.random.default_rng(0)))
        self.assertEqual(len(batches), 1)
        self.assertEqual(sorted(batches[0]), [0, 1, 2])

    def test_empty(self):
        self.assertEqual(list(minibatches(0, 4, np.random.default_rng(0))), [])

    def test_batches_are_lists_of_ints(self):
        for batch in minibatches(9, 4, np.random.default_rng(0)):
            self.assertIsInstance(batch, list)
            for i in batch:
                self.assertIs(type(i), int)

    def test_order_is_shuffled(self):
        flat = [i for batch in minibatches(100, 10, np.random.default_rng(1)) for i in batch]
        self.assertNotEqual(flat, list(range(100)))

    def test_same_seed_same_batches(self):
        a = list(minibatches(50, 8, np.random.default_rng(42)))
        b = list(minibatches(50, 8, np.random.default_rng(42)))
        self.assertEqual(a, b)

    def test_each_epoch_reshuffles(self):
        rng = np.random.default_rng(3)
        epoch1 = list(minibatches(50, 8, rng))
        epoch2 = list(minibatches(50, 8, rng))
        self.assertNotEqual(epoch1, epoch2)

    def test_rejects_bad_arguments_at_call_time(self):
        rng = np.random.default_rng(0)
        with self.assertRaises(ValueError):
            minibatches(10, 0, rng)
        with self.assertRaises(ValueError):
            minibatches(-1, 4, rng)


if __name__ == "__main__":
    unittest.main(verbosity=2)
