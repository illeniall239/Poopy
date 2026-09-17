import unittest

from solution import Autocomplete


def word_for(k):
    """"w" followed by the five digits of k (zero-padded) as the letters a..j, so numeric and alphabetical order agree."""
    return "w" + "".join(chr(97 + int(d)) for d in f"{k:05d}")


class TestAutocomplete(unittest.TestCase):
    def test_first_n_matches_in_alphabetical_order(self):
        ac = Autocomplete(["apple", "app", "application", "apt", "banana"])
        self.assertEqual(ac.suggest("app", 2), ["app", "apple"])
        self.assertEqual(ac.suggest("app", 10), ["app", "apple", "application"])
        self.assertEqual(ac.suggest("ap", 1), ["app"])

    def test_a_word_equal_to_the_prefix_comes_first(self):
        ac = Autocomplete(["card", "cart", "car"])
        self.assertEqual(ac.suggest("car", 3), ["car", "card", "cart"])

    def test_no_matches(self):
        ac = Autocomplete(["apple", "banana"])
        self.assertEqual(ac.suggest("c", 3), [])
        self.assertEqual(ac.suggest("apples", 3), [])
        self.assertEqual(ac.suggest("b", 3), ["banana"])

    def test_n_of_zero(self):
        ac = Autocomplete(["apple"])
        self.assertEqual(ac.suggest("app", 0), [])
        self.assertEqual(ac.suggest("", 0), [])

    def test_empty_prefix_gives_the_first_n_words_overall(self):
        ac = Autocomplete(["dog", "cat", "bird"])
        self.assertEqual(ac.suggest("", 2), ["bird", "cat"])
        self.assertEqual(ac.suggest("", 5), ["bird", "cat", "dog"])

    def test_duplicates_are_stored_once(self):
        ac = Autocomplete(["a", "ab", "a", "ab", "a"])
        self.assertEqual(ac.suggest("a", 5), ["a", "ab"])

    def test_insertion_order_does_not_matter_and_the_input_is_not_changed(self):
        words = ["band", "bandana", "banana", "ban"]
        ac = Autocomplete(words)
        self.assertEqual(ac.suggest("ban", 3), ["ban", "banana", "band"])
        self.assertEqual(words, ["band", "bandana", "banana", "ban"])

    def test_30000_words_and_30000_queries_without_scanning_the_list(self):
        w_count = 30000
        words = [word_for((i * 7919) % w_count) for i in range(w_count)]
        ac = Autocomplete(words)
        got = []
        expected = []
        for q in range(w_count):
            k = (q * 104729) % w_count
            base = k - k % 100
            got.append(ac.suggest(word_for(k)[:4], 3))
            expected.append([word_for(base), word_for(base + 1), word_for(base + 2)])
        self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
