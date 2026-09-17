# Sorted pair sum

Topic: 5. Two pointers
Difficulty: 1 of 3

## Problem

Write `sortedPairSum(values: number[], target: number): [number, number] | null`.

`values` is sorted in non-decreasing order. Return two values from two different positions that add up to `target`, as a pair `[smaller, larger]`. A value that appears at two positions may be used twice (`[3, 3]` with target 6), but a single position can't.

If several pairs of values work, return the one with the smallest first value. If no pair works, return `null`.

Use the sortedness: O(n) time and O(1) extra space, no `Map` or `Set`. Don't change `values`.

## Examples

```
sortedPairSum([1, 2, 3, 4, 6], 6)      → [2, 4]
sortedPairSum([1, 2, 3, 4], 5)         → [1, 4]      not [2, 3]: 1 < 2
sortedPairSum([2, 3, 4], 6)            → [2, 4]      not [3, 3]: 3 is at one position only
sortedPairSum([3, 3], 6)               → [3, 3]
sortedPairSum([-5, -2, 0, 4, 9], 2)    → [-2, 4]
sortedPairSum([1, 2, 3], 100)          → null
sortedPairSum([], 0)                   → null
```

## Constraints

- `values` has 0 to 400000 integers in non-decreasing order, each between -10^9 and 10^9; `target` is between -2 × 10^9 and 2 × 10^9.
- Time: O(n). Checking every pair is far too slow.
- Extra space: O(1).

## Hints

1. Add the smallest value to the largest value. If that sum is too small, which of the two can be safely given up on, and why can't the other one be?
2. If the sum is too big instead, which end moves? What single condition ends the loop with no pair found?
3. Why does this never miss a pair? Suppose the correct pair is somewhere in the middle: argue that neither pointer can step past its half of that pair before the other pointer reaches it.
4. In `[1, 2, 3, 4]` with target 5, why does this scheme find `[1, 4]` before `[2, 3]`?

## Explain-back

- Why does moving one pointer discard a whole set of pairs at once, and which pairs exactly?
- What happens if your loop condition allows both pointers to sit on the same index? Which example would break?
- What are the time and extra space complexity of your solution, and of the hash-map solution from Topic 4? When is the two-pointer version the better choice?
- What would change if `values` were not sorted? What would it cost to fix that first?
