# Longest common subsequence

Topic: 16. Dynamic programming
Difficulty: 3 of 3

## Problem

A subsequence of a string is what remains after deleting any number of characters (possibly none) without changing the order of the rest. `"ace"` is a subsequence of `"abcde"`; `"aec"` is not.

Write `longestCommonSubsequence(a, b)` that returns the length of the longest string that is a subsequence of both `a` and `b`. If they share no characters, or either is empty, the answer is `0`. Characters are compared exactly, so `"A"` and `"a"` are different.

## Examples

```
longestCommonSubsequence("abcde", "ace")        → 3    ("ace")
longestCommonSubsequence("abc", "def")          → 0
longestCommonSubsequence("AGGTAB", "GXTXAYB")   → 4    ("GTAB")
longestCommonSubsequence("", "abc")             → 0
```

## Constraints

- 0 ≤ `a.length`, `b.length` ≤ 1000.
- O(a.length × b.length) time. The tests include two strings of 1000 characters (400 in Python), where plain recursion that tries both options at every mismatch never finishes.

## Hints

1. Compare the last characters of `a` and `b`. If they are equal, what can you say about the answer compared with the answer for both strings without that last character?
2. If the last characters differ, at least one of them is not in the common subsequence. Which two smaller problems does that give you, and how do you combine their answers?
3. Every smaller problem is described by how many characters of `a` and how many of `b` you are still considering. How many different such problems are there in total?
4. If you store answers in a table indexed by those two lengths, which cells must already be filled before you can fill cell (i, j)? In what order does that let you fill the table?

## Explain-back

- What does dp[i][j] mean in your solution, what are the base cases, and what is the recurrence for equal and unequal characters?
- Why is plain recursion exponential here, and why is your solution O(a.length × b.length) time? What is its space?
- In what order do you fill the table, and what would go wrong if you filled it in an order that reads cells not yet computed?
- Could you use only two rows of the table instead of the whole thing? What would you give up?
