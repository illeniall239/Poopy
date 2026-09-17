import unittest

from solution import StringHashMap


class TestStringHashMap(unittest.TestCase):
    def test_set_and_get_missing_keys_give_none(self):
        m = StringHashMap()
        m.set("apple", 1)
        m.set("pear", 2)
        self.assertEqual(m.get("apple"), 1)
        self.assertEqual(m.get("pear"), 2)
        self.assertIsNone(m.get("plum"))
        self.assertEqual(m.size(), 2)
        self.assertEqual(m.bucket_count(), 8)

    def test_setting_an_existing_key_replaces_the_value_not_the_size(self):
        m = StringHashMap()
        m.set("k", "old")
        m.set("k", "new")
        self.assertEqual(m.get("k"), "new")
        self.assertEqual(m.size(), 1)

    def test_keys_with_the_same_characters_and_the_empty_key_are_all_distinct(self):
        m = StringHashMap()
        for key, value in [("ab", 1), ("ba", 2), ("listen", 3), ("silent", 4), ("", 5)]:
            m.set(key, value)
        self.assertEqual([m.get("ab"), m.get("ba"), m.get("listen"), m.get("silent"), m.get("")], [1, 2, 3, 4, 5])
        self.assertEqual(m.size(), 5)

    def test_has_is_true_for_stored_falsy_values(self):
        m = StringHashMap()
        m.set("zero", 0)
        m.set("nothing", None)
        self.assertTrue(m.has("zero"))
        self.assertTrue(m.has("nothing"))
        self.assertFalse(m.has("other"))
        self.assertEqual(m.get("zero"), 0)

    def test_delete_removes_only_that_key_and_reports_whether_it_was_there(self):
        m = StringHashMap()
        m.set("ab", 1)
        m.set("ba", 2)
        self.assertTrue(m.delete("ab"))
        self.assertFalse(m.delete("ab"))
        self.assertFalse(m.delete("never"))
        self.assertIsNone(m.get("ab"))
        self.assertFalse(m.has("ab"))
        self.assertEqual(m.get("ba"), 2)
        self.assertEqual(m.size(), 1)
        m.set("ab", 7)
        self.assertEqual(m.size(), 2)

    def test_doubles_the_buckets_only_when_the_load_factor_passes_0_75(self):
        m = StringHashMap()
        counts = []
        for i in range(1, 14):
            m.set(f"k{i}", i)
            m.set(f"k{i}", i + 100)
            counts.append(m.bucket_count())
        self.assertEqual(counts, [8, 8, 8, 8, 8, 8, 16, 16, 16, 16, 16, 16, 32])

    def test_every_entry_survives_resizing(self):
        m = StringHashMap()
        for i in range(100):
            m.set(f"item-{i}", i * i)
        wrong = [f"item-{i}" for i in range(100) if m.get(f"item-{i}") != i * i]
        self.assertEqual(wrong, [])
        self.assertEqual(m.size(), 100)
        self.assertEqual(m.bucket_count(), 256)

    def test_50000_keys_with_o_1_average_operations(self):
        m = StringHashMap()
        n = 50000
        for i in range(n):
            m.set(f"key{i}", i)
        wrong = sum(1 for i in range(n) if m.get(f"key{i}") != i)
        self.assertEqual(wrong, 0)
        self.assertEqual(m.size(), n)
        self.assertEqual(m.bucket_count(), 131072)


if __name__ == "__main__":
    unittest.main(verbosity=2)
