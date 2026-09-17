# Digit sum until single

Topic: 4. Loops and tracing code by hand
Difficulty: 2 of 3

## Problem

Write `digitSumUntilSingle(n)` that adds up the digits of `n`, then adds up the digits of that result, and keeps going until only one digit is left. Return that digit.

If `n` already has one digit, return it unchanged.

## Examples

```
digitSumUntilSingle(16)      → 7    (1 + 6 = 7)
digitSumUntilSingle(493193)  → 2    (4 + 9 + 3 + 1 + 9 + 3 = 29, 2 + 9 = 11, 1 + 1 = 2)
digitSumUntilSingle(10)      → 1
digitSumUntilSingle(0)       → 0
```

## Constraints

- `n` is a whole number from 0 to 9007199254740991 (`Number.MAX_SAFE_INTEGER`).
- Work with the number using arithmetic; don't convert it to a string.

## Hints

1. Split this into two smaller problems. First: how would you add up the digits of a number just once? Solve that before anything else.
2. For one pass over `493193`, which operator gives you the last digit? Which expression removes the last digit? Trace a table with the number and the running sum after each step.
3. When should the "one pass" loop stop? What happens to the number when you remove the last digit from `7`?
4. The outer loop repeats passes while the number has more than one digit. What is the smallest number with two digits, and so which comparison is exactly right? Check it with `10` and with `9`.

## Explain-back

- Show your tracing table for `493193`. Which variables change in the inner loop, and which only in the outer loop?
- For input `7`, how many times does each loop body run? How do you know your loops always stop?
- If the outer condition were `n > 10` instead of what you wrote, which input would give the wrong answer?
