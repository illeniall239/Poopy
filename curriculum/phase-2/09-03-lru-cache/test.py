import unittest

from solution import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_evicts_the_least_recently_used_entry_when_full(self):
        cache = LRUCache(2)
        cache.put(1, 100)
        cache.put(2, 200)
        got1 = cache.get(1)
        cache.put(3, 300)
        self.assertEqual([got1, cache.get(2), cache.get(1), cache.get(3)], [100, -1, 100, 300])

    def test_missing_key_returns_minus_1(self):
        cache = LRUCache(3)
        self.assertEqual(cache.get(42), -1)
        cache.put(1, 5)
        self.assertEqual(cache.get(2), -1)

    def test_put_on_an_existing_key_updates_the_value_without_evicting(self):
        cache = LRUCache(2)
        cache.put(1, 100)
        cache.put(2, 200)
        cache.put(1, 111)
        self.assertEqual([cache.get(1), cache.get(2)], [111, 200])

    def test_put_on_an_existing_key_counts_as_a_use(self):
        cache = LRUCache(2)
        cache.put(1, 100)
        cache.put(2, 200)
        cache.put(1, 111)
        cache.put(3, 300)
        self.assertEqual([cache.get(2), cache.get(1), cache.get(3)], [-1, 111, 300])

    def test_get_counts_as_a_use_but_a_missing_get_does_not(self):
        cache = LRUCache(2)
        cache.put(1, 100)
        cache.put(2, 200)
        cache.get(1)
        cache.get(9)
        cache.put(3, 300)
        self.assertEqual([cache.get(2), cache.get(1), cache.get(3)], [-1, 100, 300])

    def test_capacity_1_keeps_only_the_latest_entry(self):
        cache = LRUCache(1)
        cache.put(1, 100)
        cache.put(2, 200)
        self.assertEqual([cache.get(1), cache.get(2)], [-1, 200])

    def test_0_is_a_stored_value_not_a_missing_one(self):
        cache = LRUCache(2)
        cache.put(0, 0)
        cache.put(7, 0)
        self.assertEqual([cache.get(0), cache.get(7)], [0, 0])

    def test_longer_sequence_of_mixed_calls(self):
        cache = LRUCache(3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        cache.get(1)
        cache.put(4, 4)
        cache.get(3)
        cache.put(5, 5)
        cache.put(1, 10)
        cache.put(6, 6)
        self.assertEqual([cache.get(k) for k in [1, 2, 3, 4, 5, 6]], [10, -1, -1, -1, 5, 6])

    def test_30000_entries_and_260000_calls_in_constant_time_each(self):
        cap = 30000
        calls = 200000
        cache = LRUCache(cap)
        for k in range(cap):
            cache.put(k, 2 * k)
        wrong = 0
        for i in range(calls):
            k = (i * 7919) % cap
            if cache.get(k) != 2 * k:
                wrong += 1
        # The last get touched this key, so it is the most recently used.
        newest = ((calls - 1) * 7919) % cap
        for k in range(cap, 2 * cap - 1):
            cache.put(k, 2 * k)
        if cache.get(newest) != 2 * newest:
            wrong += 1
        for k in range(0, cap, 997):
            if k != newest and cache.get(k) != -1:
                wrong += 1
        for k in range(cap, 2 * cap - 1, 991):
            if cache.get(k) != 2 * k:
                wrong += 1
        self.assertEqual(wrong, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
