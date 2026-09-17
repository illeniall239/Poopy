# Running average

Topic: 6. Arrays and accumulator patterns
Difficulty: 2 of 3

## Problem

A fitness app shows your average step count after each day of the week, not just at the end.

Write `runningAverages(nums)` that returns a new array of the same length. The element at index `i` is the average of `nums[0]` through `nums[i]` (inclusive). Do not round the averages.

An empty input returns an empty array. Do not change the input array, and do not use higher-order functions like `map` or `reduce`.

## Examples

```
runningAverages([1, 2, 3, 4])   → [1, 1.5, 2, 2.5]
runningAverages([10, -10, 6])   → [10, 0, 2]
runningAverages([5])            → [5]
runningAverages([])             → []
```

## Constraints

- `nums` has 0 to 100000 elements.
- Every element is a finite number (it may be negative).
- The input array must not be modified.
- Your solution should look at each element a constant number of times (no re-adding the whole prefix for every index).

## Hints

1. Work out `[1, 2, 3, 4]` by hand. At each step, which two numbers did you divide?
2. When you move from index 2 to index 3, what do you already know that saves you re-adding 1, 2 and 3?
3. There are two accumulators here: one for the result array and one for something else. What is the something else, and what does it start at?
4. At index `i`, how many elements have been included so far? Check your answer against index 0.

## Explain-back

- Why do you divide by `i + 1` and not by `nums.length` or by `i`?
- What would happen to the running time if you re-added the prefix from the start at every index, for 100000 elements?
- Your function returns a new array. Why is that better than writing the averages back into `nums`?
