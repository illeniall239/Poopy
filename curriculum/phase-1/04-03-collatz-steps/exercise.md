# Collatz steps

Topic: 4. Loops and tracing code by hand
Difficulty: 3 of 3

## Problem

The Collatz sequence starts from a whole number `n` and repeats one step:

- if the number is even, divide it by 2;
- if the number is odd, multiply it by 3 and add 1.

It stops when the number reaches 1.

Write `collatzSteps(n)` that returns `{ steps, peak }`:

- `steps` is how many steps it takes to reach 1.
- `peak` is the largest number that appears in the sequence, including `n` itself.

## Examples

```
collatzSteps(6)  → { steps: 8, peak: 16 }     (6, 3, 10, 5, 16, 8, 4, 2, 1)
collatzSteps(1)  → { steps: 0, peak: 1 }
collatzSteps(2)  → { steps: 1, peak: 2 }
collatzSteps(27) → { steps: 111, peak: 9232 }
```

## Constraints

- `n` is a whole number from 1 to 1000000.

## Hints

1. Write out the sequence for `6` by hand. Count the arrows between numbers, not the numbers. Why are those two counts different?
2. Make a tracing table for `n = 6` with columns for the current number, `steps` and `peak`. What values go in the first row, before any step happens?
3. You don't know in advance how many steps there will be. Which kind of loop fits that? What exactly is its condition, and what happens to it when `n` is `1`?
4. Inside the loop, in what order do you change the number, count the step and update the peak? Does your table still give `peak: 16` for `6` and `peak: 1` for `1`?

## Explain-back

- Show your tracing table for `n = 6`. What is true about `peak` at the end of every iteration?
- For `n = 1`, how many times does your loop body run? Why is that the right number?
- What would your loop do if someone passed `0`? Why?
