# Longest unique substring

Topic: 6. Sliding window
Difficulty: 2 of 3

## Problem

Write `longestUniqueSubstring(s: string): number`. Return the length of the longest substring of `s` in which no character appears twice.

- A substring is contiguous; `"ace"` is not a substring of `"abcde"`.
- Any character can appear, not just letters: spaces, digits, punctuation and characters far beyond ASCII. Two characters are the same when `===` says so.
- The empty string gives 0.

## Examples

```
longestUniqueSubstring("abcabcbb")   → 3       "abc"
longestUniqueSubstring("bbbbb")      → 1
longestUniqueSubstring("pwwkew")     → 3       "wke"; "pwke" is not a substring
longestUniqueSubstring("abba")       → 2
longestUniqueSubstring("")           → 0
```

## Constraints

- `s` has 0 to 100000 characters, each any UTF-16 code unit.
- Time: O(n). Growing a substring from every start position is O(n · answer) and too slow when the answer is large.
- Extra space: O(k) where k is the number of distinct characters.

## Hints

1. Keep a window `s[left..right]` with no repeats. When the character at `right + 1` is already in the window, what is the smallest move of `left` that makes room for it?
2. What could you store per character so that "where did I last see this?" is O(1)? How does that let `left` jump instead of stepping?
3. In `"abba"`, when `right` reaches the final `a`, the last position of `a` is 0 but `left` is already past it. What must you never do to `left`?
4. When exactly do you record a candidate answer, and how do you compute the window length from `left` and `right` without an off-by-one?

## Explain-back

- Why does the window version do O(n) work in total, when each step may move `left` several positions?
- What breaks in `"abba"` if `left` is allowed to move backwards, and what result would you get?
- What are the time and extra space complexity of your solution? What is k for a string of lowercase letters, and for arbitrary text?
- If you replaced the `Map` with an array of 26 slots, what inputs would break, and would the big test still pass?
