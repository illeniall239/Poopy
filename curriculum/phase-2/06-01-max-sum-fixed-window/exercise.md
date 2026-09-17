# Max sum of a fixed window

Topic: 6. Sliding window
Difficulty: 1 of 3

## Problem

A fitness app shows the best `k`-day stretch: the `k` consecutive days with the highest total step count.

Write `maxSumFixedWindow(values: number[], k: number): number`. Return the largest sum of any `k` consecutive elements of `values`.

- `k` is at least 1. If `values` has fewer than `k` elements, there is no window: return 0.
- Values may be negative, so the answer may be negative too.
- Don't change `values`.

## Examples

```
maxSumFixedWindow([2, 1, 5, 1, 3, 2], 3)      → 9       5 + 1 + 3
maxSumFixedWindow([2, 3, 4, 1, 5], 2)         → 7
maxSumFixedWindow([-1, -2, -3, -4], 2)        → -3
maxSumFixedWindow([1, 2, 3], 3)               → 6
maxSumFixedWindow([1, 2], 3)                  → 0
```

## Constraints

- `values` has 0 to 400000 integers, each between -10^4 and 10^4; `k` is between 1 and 400000.
- Time: O(n). Re-adding all `k` elements for every window is O(n·k) and too slow when `k` is large.
- Extra space: O(1).

## Hints

1. Write out the windows of size 3 for `[2, 1, 5, 1, 3, 2]`. How much do two neighbouring windows have in common?
2. Given the sum of the window starting at `i`, what two numbers turn it into the sum of the window starting at `i + 1`?
3. How do you get the very first sum, and from which index does the sliding start?
4. Before the loop, what should happen when `k` is larger than the array? What does the loop do in that case if you don't check?

## Explain-back

- Why is the sliding version O(n) and the recompute-every-window version O(n·k)? For which `k` is the difference biggest?
- Where is the off-by-one risk when you slide: which element leaves and which enters when the window starts at `i`?
- What are the time and extra space complexity of your solution?
- Could the same idea answer "the largest average of k consecutive elements"? What about "the largest product"? Which one breaks and why?
