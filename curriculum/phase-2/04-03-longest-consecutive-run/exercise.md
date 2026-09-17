# Longest consecutive run

Topic: 4. Arrays and hashing
Difficulty: 2 of 3

## Problem

A run is a set of integers with no gaps: `5, 6, 7, 8` is a run of length 4. The integers of a run may sit anywhere in the array, in any order.

Write `longestConsecutiveRun(values: number[]): number`. Return the length of the longest run that can be formed from the values in `values`.

- A value that appears several times counts once: `[1, 2, 2, 3]` gives 3.
- Every non-empty array has a run of at least 1. An empty array gives 0.
- Don't change `values`.

## Examples

```
longestConsecutiveRun([100, 4, 200, 1, 3, 2])           → 4      1, 2, 3, 4
longestConsecutiveRun([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])   → 9      0 through 8
longestConsecutiveRun([10, 30, 20])                     → 1
longestConsecutiveRun([-1, 0, 1, -3, -2])               → 5
longestConsecutiveRun([])                               → 0
```

## Constraints

- `values` has 0 to 400000 integers, each between -10^9 and 10^9.
- Time: O(n). Sorting is O(n log n) and doesn't count; walking up from every value is O(n²) in the worst case.
- Extra space: O(n).

## Hints

1. If you could ask "is the value v in the array?" in O(1), how would you count the length of the run that contains v?
2. In `[1, 2, 3, 4]`, walking up from 1, from 2, from 3 and from 4 counts the same run four times. Which of those four values is the only one worth starting from, and how can you tell it apart in O(1)?
3. If you only start counting from values that begin a run, how many times can each value be visited in total across all the walks? What does that make the total time?
4. What does your code return for `[]`, and for `[7, 7, 7]`? Does the duplicate change the answer?

## Explain-back

- Why does starting only from values whose predecessor is absent make the whole algorithm O(n), even though it has a loop inside a loop?
- What are the time and extra space complexity of your solution, and of the sort-then-scan version? Which one would you write in an interview if O(n log n) were allowed?
- How does your solution treat duplicate values, and where in the code does that happen?
- Would a `Set` still give O(1) lookups if the values were strings instead of numbers? What about an array indexed by value?
