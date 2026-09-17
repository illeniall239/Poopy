# Sum of multiples

Topic: 4. Loops and tracing code by hand
Difficulty: 1 of 3

## Problem

Write `sumOfMultiples(n)` that returns the sum of all whole numbers from 1 up to but **not including** `n` that are divisible by 3 or by 5.

A number divisible by both 3 and 5 (like 15) is added only once.

## Examples

```
sumOfMultiples(10)  → 23      (3 + 5 + 6 + 9)
sumOfMultiples(16)  → 60      (3 + 5 + 6 + 9 + 10 + 12 + 15)
sumOfMultiples(3)   → 0
sumOfMultiples(0)   → 0
```

## Constraints

- `n` is a whole number from 0 to 100000.

## Hints

1. List by hand every number you'd check for `n = 10`. What is the first one, and what is the last one?
2. Make a tracing table for `n = 10` with columns for the loop counter and the running total. What is the total before the loop starts?
3. For `n = 3`, should the number 3 be added? Which comparison in your loop condition decides that: `<` or `<=`?
4. For `n = 16`, how many times does 15 get added in your code? What single condition says "divisible by 3 or by 5"?

## Explain-back

- Show your tracing table for `n = 10`. What is true about the running total at the end of every iteration?
- What happens to your loop when `n` is `0`? How many times does the body run?
- If you had written `<=` instead of `<`, which test would fail, and why?
