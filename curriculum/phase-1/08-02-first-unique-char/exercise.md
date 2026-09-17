# First unique character

Topic: 8. Objects, Map and Set
Difficulty: 2 of 3

## Problem

Write `firstUniqueIndex(text)` that returns the index of the first character in `text` that appears exactly once in the whole string. If no character appears exactly once (including an empty string), return `-1`.

Comparison is case-sensitive: `"a"` and `"A"` are different characters. Spaces and punctuation are characters like any other.

## Examples

```
firstUniqueIndex("leetcode")       → 0
firstUniqueIndex("loveleetcode")   → 2
firstUniqueIndex("aabb")           → -1
firstUniqueIndex("aA")             → 0
firstUniqueIndex("")               → -1
```

## Constraints

- `text` has 0 to 100000 characters.
- Your solution must be fast for 100000 characters: it should not, for every character, scan the whole string again.

## Hints

1. For `"loveleetcode"`, how did you decide by hand that `l` and `o` don't qualify but `v` does?
2. Could you answer "how many times does this character appear?" instantly if you had already done some work first? What would that work be?
3. Which structure lets you store a count for any character and look it up by that character? What do you do the first time you see a character?
4. Once the counts are ready, in what order should you look at the characters so the first one you find is the right answer?

## Explain-back

- Why does your solution walk the string twice instead of once, and why is that still fast?
- Why did you use a `Map` (or whatever you chose) rather than a `Set`? What does a `Set` not remember?
- What does `"aA"` return, and what would change if the comparison ignored case?
