# Convert between bases

Topic: 1. How computers run code
Difficulty: 1 of 3

## Problem

Computers store every number as bits, but the same value can be written in any base.

Write two functions:

- `toBase(n, base)` returns the non-negative integer `n` written in `base` (2 to 16). Digits above 9 are the lowercase letters `a` to `f`. There are no leading zeros, and `0` is written as `"0"`.
- `fromBase(text, base)` does the reverse: it reads a string of digits in `base` (lowercase letters only) and returns the number.

Do the conversion yourself with repeated division and multiplication. Don't use `n.toString(base)` or `parseInt(text, base)`.

## Examples

```
toBase(10, 2)            → "1010"
toBase(255, 16)          → "ff"
toBase(0, 7)             → "0"
fromBase("1010", 2)      → 10
fromBase("7fffffff", 16) → 2147483647
```

## Constraints

- `0 <= n <= 2147483647` (the largest 32-bit signed integer).
- `2 <= base <= 16`.
- `text` is a valid, non-empty number in `base` with no leading zeros (except `"0"` itself), and its value is at most `2147483647`.
- Time: O(number of digits), that is O(log n). Counting up from 0 is far too slow.

## Hints

1. Convert 10 to base 2 on paper by dividing by 2 again and again. Which part of each division did you write down?
2. The remainders came out in some order. Is that the order the digits appear in the answer?
3. What should your loop do when `n` starts at 0, so that you still return one digit?
4. Reading `"ff"` left to right: if you already know the value of `"f"`, how do you get the value of `"ff"` from it by taking in one more digit?

## Explain-back

- Why does the first remainder give the last digit rather than the first?
- Why is `2147483647` the largest value here? What does 32 bits have to do with it, and what does it look like in base 2?
- How many loop iterations does `toBase` do for `n` in base `b`? Why is that O(log n) time, and how much extra space does it use?
- If `2147483647` were stored in a Java `int` and you added 1, what would happen, and why doesn't a JavaScript `number` behave the same way?
