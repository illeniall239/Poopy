# Smallest covering window

Topic: 6. Sliding window
Difficulty: 3 of 3

## Problem

Write `smallestCoveringWindow(s: string, t: string): string`. Return the shortest substring of `s` that contains every character of `t`, counting repeats: if `t` has two `a`s, the substring needs at least two `a`s. Characters of the substring may appear in any order and other characters may sit between them.

- If several shortest substrings exist, return the leftmost one (smallest start index).
- If no substring of `s` covers `t`, or `t` is empty, return `""`.
- Characters are compared with `===`; upper and lower case are different characters.

## Examples

```
smallestCoveringWindow("ADOBECODEBANC", "ABC")   → "BANC"
smallestCoveringWindow("abzcxcba", "abc")        → "cba"
smallestCoveringWindow("acbxbca", "abc")         → "acb"     "bca" is as short but further right
smallestCoveringWindow("aa", "aa")               → "aa"
smallestCoveringWindow("a", "aa")                → ""
smallestCoveringWindow("abc", "")                → ""
```

## Constraints

- `s` has 0 to 400000 characters and `t` has 0 to 400000 characters, any UTF-16 code units.
- Time: O(|s| + |t|). Trying every start position is O(|s|²) and far too slow.
- Extra space: O(k) where k is the number of distinct characters in `t`.

## Hints

1. What information about `t` do you need before scanning `s`? Is "which characters" enough, or do you need "how many of each"?
2. Grow the window to the right until it covers `t`. Then what can you do with the left edge, and what tells you the window has stopped covering `t`?
3. Checking "is the window covering `t`?" by comparing two full maps at every step costs O(k) per step. What single counter could you maintain so the check is O(1)? When does it go up, and when down?
4. Where do you record the best window: while expanding, or each time you are about to shrink? Which choice makes `"acbxbca"` return the leftmost answer?

## Explain-back

- Why is the total work O(|s| + |t|) even though the left edge moves inside a loop nested in the right-edge loop?
- Explain the counter you keep for "how many required characters are satisfied". Why must it not go up when an already satisfied character appears again?
- What are the time and extra space complexity of your solution?
- What would change if characters of `t` had to appear in the window in the same order as in `t`? Would a sliding window still work?
