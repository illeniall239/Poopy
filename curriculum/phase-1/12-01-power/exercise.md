# Fast power

Topic: 12. Recursion
Difficulty: 1 of 3

## Problem

Write a recursive function `power(base, exp)` that returns `base` raised to the power `exp`, without using `**` or `Math.pow`.

Multiplying `base` by itself `exp` times is too slow and, done recursively, makes one call per step, which overflows the call stack for large `exp`. Use halving instead: `base` to the power `exp` can be built from `base` to the power `Math.floor(exp / 2)`, so each call works on an exponent about half as big as the one before.

Any number to the power `0` is `1`, including `power(0, 0)`.

## Examples

```
power(2, 10)            → 1024
power(3, 5)             → 243
power(5, 0)             → 1
power(0, 0)             → 1
power(-2, 3)            → -8
power(1, 1000000000)    → 1     (must finish instantly)
```

## Constraints

- `base` is a number from -10 to 10 (it may have decimals).
- `exp` is a whole number from 0 to 1000000000.
- Don't use `**`, `Math.pow` or loops.

## Hints

1. Before writing anything: what is the smallest `exp` whose answer you know without doing any multiplying? That's your base case.
2. Work out `power(2, 10)` by hand, but start from `power(2, 5)`. How do you get from `2^5` to `2^10` in one multiplication?
3. Now try `power(2, 11)` starting from `power(2, 5)`. What extra multiplication do you need when `exp` is odd?
4. If your function calls `power(base, exp / 2)` twice in the same call, how many calls happen in total? How can you make just one recursive call and reuse its result?

## Explain-back

- Name your base case and the smaller subproblem. How do you know every call gets closer to the base case?
- Draw the call stack for `power(2, 10)`. How many calls deep does it go, and roughly how deep would `power(1, 1000000000)` go?
- Why would `return power(base, exp - 1) * base` crash for `exp = 1000000000` even though it's correct for small `exp`?
