# Debug: dedupe

Topic: 15. Reading and debugging code
Difficulty: 3 of 3

## Problem

`dedupe(items)` is supposed to return a new array with duplicate numbers removed. Each number is kept at the position of its first appearance, and the order of the kept numbers doesn't change. The input array must not be changed, and the result is always a new array, even when there were no duplicates.

This function has a bug (or bugs). Find and fix it without rewriting it from scratch.

## Examples

```
dedupe([1, 2, 1, 3, 2])   → [1, 2, 3]
dedupe([5, 5, 5, 5])      → [5]
dedupe([3, 1, 2])         → [3, 1, 2]     (a new array, equal to the input)
dedupe([])                → []

const input = [4, 4, 7];
dedupe(input)             → [4, 7]
input                     → still [4, 4, 7]
```

## Constraints

- `items` has 0 to 10000 numbers.
- Keep the function's structure: one loop and a `Set`.

## Hints

1. Run the tests. `[1, 2, 1, 3, 2]` gives the right answer, but `[5, 5, 5, 5]` doesn't. Write down exactly what each returned.
2. Make a tracing table for `[5, 5, 5, 5]` with columns `i`, `items` (the whole array at that moment), `items[i]` and `seen`. What happens to the element right after one that gets removed?
3. One of the failing tests isn't about the returned values at all. What does it check, and which line in the function could cause that?
4. You've found that the array changes while the loop is walking over it. Is the cause the loop counter, or the fact that the array being walked over is being changed? Which fix removes the cause instead of patching around it?

## Explain-back

- What were your hypotheses, in order, and what did you run or trace to confirm or reject each one?
- Why did `[1, 2, 1, 3, 2]` come out right even though the code was wrong?
- Adding `i--` right after the removal makes the values come out right. Why would that still leave a bug, and why is changing the loop counter inside the body a fragile fix?
