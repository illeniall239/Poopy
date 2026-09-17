import unittest

from solution import is_balanced


class TestIsBalanced(unittest.TestCase):
    def test_pairs_side_by_side(self):
        self.assertIs(is_balanced("()[]{}"), True)

    def test_pairs_nested_inside_each_other(self):
        self.assertIs(is_balanced("{[()]}"), True)

    def test_wrong_kind_of_closing_bracket(self):
        self.assertIs(is_balanced("(]"), False)

    def test_pairs_that_cross_instead_of_nesting(self):
        self.assertIs(is_balanced("([)]"), False)

    def test_opening_brackets_never_closed(self):
        self.assertIs(is_balanced("(("), False)

    def test_closing_bracket_with_nothing_open(self):
        self.assertIs(is_balanced("())"), False)
        self.assertIs(is_balanced(")"), False)

    def test_other_characters_are_ignored(self):
        self.assertIs(is_balanced("f(a[0]) { x; }"), True)
        self.assertIs(is_balanced("abc"), True)

    def test_empty_string_is_balanced(self):
        self.assertIs(is_balanced(""), True)

    def test_200000_levels_deep_in_linear_time(self):
        n = 200000
        deep = ("([{" * (n // 2))[:n]
        closers = {"(": ")", "[": "]", "{": "}"}
        close = "".join(closers[c] for c in reversed(deep))
        self.assertIs(is_balanced(deep + close), True)
        self.assertIs(is_balanced(deep + close[1:]), False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
