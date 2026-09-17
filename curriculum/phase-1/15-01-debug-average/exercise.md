# Debug: average

Topic: 15. Reading and debugging code
Difficulty: 1 of 3

## Problem

`average(numbers)` is supposed to return the arithmetic mean of `numbers`: the sum of all the values divided by how many there are. The result is exact, not rounded. For an empty array it returns `undefined`.

This function has a bug (or bugs). Find and fix it without rewriting it from scratch.

Work like a detective: run the tests, pick one failing test, and form a guess about the cause before you change anything. Change one thing at a time and re-run the tests after each change.

## Examples

```
average([2, 4, 6])    → 4
average([1, 2])       → 1.5
average([5])          → 5
average([-1, -2])     → -1.5
average([])           → undefined
```

## Constraints

- `numbers` has 0 to 10000 items, each a whole number from -1000000 to 1000000.
- Keep the function's structure. The fix should be small.

## Hints

1. Run the tests. Which ones pass and which fail? What do the passing ones have in common that the failing ones don't?
2. Take the smallest failing case, `average([5])`. What did the function return? Before reading the code again, what would have to happen inside for it to return that?
3. Make a tracing table for `average([1, 2])`: one row per loop iteration, with columns for `i`, `numbers[i]` and `total`. Compare the final `total` with what you'd expect.
4. After fixing one thing, re-run the tests. If `[1, 2]` still fails, compare the value it returns with the right answer. What kind of difference is it: off by an element, or off by a fraction?

## Explain-back

- How many bugs were there? For each, what test output first pointed you at it, and what was your hypothesis?
- Why did `average([0, 0, 0])` and `average([])` pass even with the bugs present? What does that tell you about choosing test cases?
- If you'd fixed both bugs at once and a test still failed, what would have been harder to figure out?
