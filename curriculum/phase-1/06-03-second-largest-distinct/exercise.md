# Second largest distinct value

Topic: 6. Arrays and accumulator patterns
Difficulty: 3 of 3

## Problem

A leaderboard wants to show the runner-up score. Several players can share the top score, so the runner-up is the second largest *distinct* value.

Write `secondLargest(nums)` that returns the second largest distinct value in the array. If the array has fewer than two distinct values (including an empty array), return `undefined`.

Do not change the input array. Do not sort, and do not use `Math.max`, `Set`, or higher-order functions. Use a single loop.

## Examples

```
secondLargest([3, 1, 2])        → 2
secondLargest([5, 5, 4])        → 4
secondLargest([-1, -3, -2])     → -2
secondLargest([7, 7, 7])        → undefined
secondLargest([])               → undefined
```

## Constraints

- `nums` has 0 to 100000 elements.
- Every element is a finite number (it may be negative).
- The input array must not be modified.

## Hints

1. Scanning left to right, how many values do you need to remember at each step? What are they?
2. Trace `[1, 3, 2]` by hand. When you see `3`, what happens to the value that used to be the largest?
3. Trace `[5, 5, 4]`. When you see the second `5`, which of your remembered values should change, if any?
4. Before you've seen anything, what starting values can never be mistaken for a real element? At the end, how do you tell "no second value was found" apart from a real answer?

## Explain-back

- Why would starting both trackers at `0` break for `[-1, -3, -2]`?
- In your loop, what happens when a value equals the current largest, and why?
- Sorting a copy would also work. What does sorting cost compared to your single pass, and what would go wrong if you sorted `nums` itself?
