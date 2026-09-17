import unittest

from solution import WordDictionary


def encode(x):
    """Five lowercase letters encoding x (0 <= x < 26**5), most significant first."""
    s = ""
    for _ in range(5):
        s = chr(97 + x % 26) + s
        x //= 26
    return s


class TestWordDictionary(unittest.TestCase):
    def test_dots_match_any_single_letter(self):
        d = WordDictionary()
        for w in ["bad", "dad", "mad"]:
            d.add_word(w)
        self.assertFalse(d.search("pad"))
        self.assertTrue(d.search("bad"))
        self.assertTrue(d.search(".ad"))
        self.assertTrue(d.search("b.."))

    def test_lengths_must_match(self):
        d = WordDictionary()
        d.add_word("cat")
        self.assertFalse(d.search("ca"))
        self.assertFalse(d.search("c."))
        self.assertFalse(d.search("c.t."))
        self.assertFalse(d.search("cats"))

    def test_empty_dictionary(self):
        d = WordDictionary()
        self.assertFalse(d.search("a"))
        self.assertFalse(d.search("."))

    def test_a_query_of_only_dots_matches_any_word_of_that_length(self):
        d = WordDictionary()
        d.add_word("hello")
        self.assertTrue(d.search("....."))
        self.assertFalse(d.search("...."))
        self.assertFalse(d.search("......"))

    def test_every_branch_under_a_dot_is_tried(self):
        d = WordDictionary()
        for w in ["abc", "abd", "abx"]:
            d.add_word(w)
        self.assertTrue(d.search("ab."))
        self.assertTrue(d.search("a.x"))
        self.assertFalse(d.search("a.y"))
        self.assertFalse(d.search("b.."))

    def test_dots_at_the_start_and_two_dots(self):
        d = WordDictionary()
        d.add_word("cab")
        d.add_word("dab")
        self.assertTrue(d.search(".ab"))
        self.assertTrue(d.search("..b"))
        self.assertFalse(d.search("..c"))
        self.assertTrue(d.search(".a."))

    def test_a_prefix_of_a_stored_word_is_not_a_match(self):
        d = WordDictionary()
        d.add_word("dog")
        d.add_word("dog")
        d.add_word("dogs")
        self.assertFalse(d.search("do"))
        self.assertFalse(d.search("d."))
        self.assertTrue(d.search("dog"))
        self.assertTrue(d.search("d.g"))
        self.assertTrue(d.search("do.s"))

    def test_20000_words_and_60000_searches_without_scanning_the_words(self):
        w_count = 20000
        d = WordDictionary()
        words = set()
        tail_masked = set()
        head_masked = set()
        word_list = []
        for i in range(w_count):
            w = encode((i * 7919) % 1000003)
            word_list.append(w)
            words.add(w)
            tail_masked.add(w[:4])
            head_masked.add(w[1:])
            d.add_word(w)
        expected = []
        got = []
        for q in range(w_count):
            s = word_list[q] if q % 2 == 0 else encode((q * 104729) % 1000003)
            expected += [s in words, s[:4] in tail_masked, s[1:] in head_masked]
            got += [d.search(s), d.search(s[:4] + "."), d.search("." + s[1:])]
        self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
