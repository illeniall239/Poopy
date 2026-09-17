# Compress runs

Topic: 7. Strings
Difficulty: 2 of 3

## Problem

A run is a group of the same character repeated back to back. `"aaabcc"` has three runs: `aaa`, `b` and `cc`.

Write `compressRuns(text)` that returns a new string where each run is replaced by its character followed by the run length. If a run has length 1, write only the character (no `1`).

Comparison is case-sensitive: `"a"` and `"A"` are different characters. An empty string returns `""`.

## Examples

```
compressRuns("aaabcc")        → "a3bc2"
compressRuns("abc")           → "abc"
compressRuns("aabbaa")        → "a2b2a2"
compressRuns("aAA")           → "aA2"
compressRuns("")              → ""
```

## Constraints

- `text` has 0 to 100000 characters.
- `text` contains no digits.

## Hints

1. Compress `"aabbaa"` by hand. How did you know when one run ended and the next began?
2. As you walk through the string, what two things do you need to remember about the run you're currently in?
3. When the current character differs from the previous one, what must happen before you start counting the new run?
4. After the loop ends, has the last run been written out yet? Try your plan on `"abcc"` and check the final `c2`.

## Explain-back

- Why doesn't `"a"` equal `"A"` in your comparison, and how would you change the rules to make it case-insensitive?
- How does your code make sure the final run is included?
- Strings can't be changed in place. How does your code build the result, and what does it do for the empty string?
