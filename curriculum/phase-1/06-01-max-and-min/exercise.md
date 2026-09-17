# Max and min

Topic: 6. Arrays and accumulator patterns
Difficulty: 1 of 3

## Problem

Write `maxAndMin(nums)` that returns the largest and smallest value in an array of numbers, as `{ max, min }` (type `MaxMin`).

If the array is empty there is no largest or smallest value, so return `undefined`.

Do not change the input array, and do not use `Math.max`, `Math.min`, sorting, or higher-order functions like `reduce`. Use a loop.

## Examples

```
maxAndMin([3, 9, 1, 4])     → { max: 9, min: 1 }
maxAndMin([-5, -2, -8])     → { max: -2, min: -8 }
maxAndMin([7])              → { max: 7, min: 7 }
maxAndMin([])               → undefined
```

## Constraints

- `nums` has 0 to 100000 elements.
- Every element is a finite number (it may be negative or a decimal).
- The input array must not be modified.

## Hints

1. Scanning the list `[3, 9, 1, 4]` by eye, what do you keep in your head as you move from one number to the next?
2. Before you have looked at any number, what should "the largest so far" be? Try your idea on `[-5, -2, -8]` by hand.
3. Is there a value in the array itself that is always a safe starting point for both the largest and the smallest? When does that value not exist?
4. Once you have a starting point, what single comparison per element decides whether "largest so far" changes? And for "smallest so far"?

## Explain-back

- What would your function return for `[-5, -2, -8]` if you had started `max` at `0`? Why is that wrong?
- What is `nums[0]` when `nums` is empty, and how does your code avoid using it?
- How do you know your function leaves the caller's array exactly as it was?
