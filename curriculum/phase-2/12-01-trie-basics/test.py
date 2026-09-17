import unittest

from solution import Trie


def encode(x):
    """Five lowercase letters encoding x (0 <= x < 26**5), most significant first."""
    s = ""
    for _ in range(5):
        s = chr(97 + x % 26) + s
        x //= 26
    return s


class TestTrie(unittest.TestCase):
    def test_whole_word_versus_its_beginning(self):
        trie = Trie()
        trie.insert("apple")
        self.assertTrue(trie.search("apple"))
        self.assertFalse(trie.search("app"))
        self.assertTrue(trie.starts_with("app"))

    def test_a_prefix_becomes_a_word_once_inserted(self):
        trie = Trie()
        trie.insert("apple")
        trie.insert("app")
        self.assertTrue(trie.search("app"))
        self.assertTrue(trie.search("apple"))

    def test_empty_trie_answers_false(self):
        trie = Trie()
        self.assertFalse(trie.search("a"))
        self.assertFalse(trie.starts_with("a"))

    def test_words_sharing_a_beginning(self):
        trie = Trie()
        for w in ["car", "cart", "cat"]:
            trie.insert(w)
        self.assertTrue(trie.search("car"))
        self.assertTrue(trie.search("cart"))
        self.assertTrue(trie.search("cat"))
        self.assertFalse(trie.search("ca"))
        self.assertTrue(trie.starts_with("ca"))
        self.assertFalse(trie.starts_with("cab"))
        self.assertTrue(trie.starts_with("cart"))

    def test_inserting_the_same_word_twice_changes_nothing(self):
        trie = Trie()
        trie.insert("dog")
        trie.insert("dog")
        self.assertTrue(trie.search("dog"))
        self.assertFalse(trie.search("do"))
        self.assertTrue(trie.starts_with("dog"))

    def test_query_longer_than_any_stored_word(self):
        trie = Trie()
        trie.insert("cat")
        self.assertFalse(trie.search("cats"))
        self.assertFalse(trie.starts_with("cats"))

    def test_different_first_letters(self):
        trie = Trie()
        for w in ["dog", "dot", "cat"]:
            trie.insert(w)
        self.assertTrue(trie.starts_with("d"))
        self.assertTrue(trie.starts_with("c"))
        self.assertFalse(trie.starts_with("e"))
        self.assertFalse(trie.search("d"))

    def test_20000_words_and_40000_queries_in_linear_time_each(self):
        w_count = 20000
        trie = Trie()
        words = set()
        prefixes = set()
        word_list = []
        for i in range(w_count):
            w = encode((i * 7919) % 1000003)
            word_list.append(w)
            words.add(w)
            prefixes.add(w[:4])
            trie.insert(w)
        expected = []
        got = []
        for q in range(w_count):
            s = word_list[q] if q % 2 == 0 else encode((q * 104729) % 1000003)
            expected += [s in words, s[:4] in prefixes]
            got += [trie.search(s), trie.starts_with(s[:4])]
        self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
