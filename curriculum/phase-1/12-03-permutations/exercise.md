# Permutations

Topic: 12. Recursion
Difficulty: 3 of 3

## Problem

Write a recursive function `permutations(s)` that returns every distinct way to order the characters of the string `s`.

- Each result uses every character of `s` exactly once.
- If `s` has repeated characters, orderings that produce the same string appear only once.
- The result is sorted in ascending order (the order JavaScript's default `sort()` gives for strings).
- The empty string has exactly one ordering: `""`.

## Examples

```
permutations("ab")    → ["ab", "ba"]
permutations("abc")   → ["abc", "acb", "bac", "bca", "cab", "cba"]
permutations("aab")   → ["aab", "aba", "baa"]
permutations("a")     → ["a"]
permutations("")      → [""]
```

## Constraints

- `s` has 0 to 8 characters.

## Hints

1. Do `"abc"` by hand. What choice do you make first, and what's left to arrange after you make it?
2. Once you've picked the first character, arranging the rest is the same problem on a shorter string. What string exactly, and how do you build it from `s` without the character you picked?
3. What should the function return for the shortest possible string so that the longer cases build on it correctly? Check it against `"a"` and `"ab"`.
4. With `"aab"`, picking the first `a` and picking the second `a` lead to the same strings. Where can you remove duplicates: while building, or once at the end?

## Explain-back

- What's your base case, and why is returning `[""]` different from returning `[]` there? Trace `"a"` both ways.
- How many calls does `permutations("abc")` make in total? Sketch the tree of calls.
- For an 8-character string there are 40320 results. What does that say about how fast this grows, and when would recursion like this be a bad idea?
