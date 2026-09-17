# Search a rotated sorted array

Topic: 8. Binary search
Difficulty: 3 of 3

## Problem

A circular log buffer keeps entry numbers in increasing order, but the oldest entry isn't always at index 0: the array was sorted and then rotated, so it looks like `[40, 50, 60, 10, 20, 30]`.

Write `searchRotated(nums: number[], target: number): number`.

- `nums` holds distinct whole numbers. It is a strictly increasing array that has been rotated by some unknown amount from 0 to `nums.length - 1`: its last k elements were moved, in order, to the front. A rotation of 0 leaves it fully sorted.
- Return the index of `target` in `nums`, or `-1` if it isn't there.

Don't change `nums`, don't use any built-in search, and don't search the whole array one element at a time.

## Examples

```
searchRotated([40, 50, 60, 10, 20, 30], 20)  → 4
searchRotated([40, 50, 60, 10, 20, 30], 50)  → 1
searchRotated([40, 50, 60, 10, 20, 30], 35)  → -1
searchRotated([10, 20, 30, 40], 30)          → 2
searchRotated([7], 7)                        → 0
searchRotated([], 7)                         → -1
```

## Constraints

- `nums` has 0 to 1000000 elements; values and `target` are whole numbers from -2000000000 to 2000000000.
- Required: O(log n) time per call and O(1) extra space.
- The large test makes 100000 calls on an array of 1000000 values, so scanning the array is too slow.

## Hints

1. Cut `[40, 50, 60, 10, 20, 30]` at any middle index. Look at the two halves. Is at least one of them always in sorted order? Try a few different cut points.
2. How can you tell, using only `nums[lo]`, `nums[mid]` and `nums[hi]`, which half is the sorted one?
3. Once you know which half is sorted, what two comparisons tell you whether `target` must be inside that half?
4. If `target` isn't inside the sorted half, where must it be, if it's anywhere? Check your comparisons against a half with just one element, where `lo === mid`.

## Explain-back

- Why is one of the two halves always sorted, whatever the rotation?
- Walk through searching `[40, 50, 60, 10, 20, 30]` for `20`, giving `lo`, `mid` and `hi` at each step.
- Which comparison in your code uses `<=` rather than `<`, and what input breaks if you change it?
- What are the time and space complexity? Why wouldn't "find the rotation point by scanning, then binary search" meet the requirement?
