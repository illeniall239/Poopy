# Pair with target sum

Topic: 4. Arrays and hashing
Difficulty: 1 of 3

## Problem

Write `pairWithTargetSum(values: number[], target: number): [number, number]`.

Return the indices `[i, j]` of two different positions, `i < j`, with `values[i] + values[j] === target`. The two positions may hold equal values, but one position can't be used twice.

If several pairs work, return the one with the smallest `j`; if several pairs share that `j`, the one with the smallest `i`. If no pair works, return `[-1, -1]`.

Scan the array once. Don't change `values`.

## Examples

```
pairWithTargetSum([2, 7, 11, 15], 9)     → [0, 1]
pairWithTargetSum([3, 2, 4], 6)          → [1, 2]      not [0, 0]
pairWithTargetSum([2, 2, 4], 6)          → [0, 2]      [1, 2] has the same j but a larger i
pairWithTargetSum([1, 3, 2, 4, 3], 6)    → [2, 3]      [1, 4] has a larger j
pairWithTargetSum([5], 10)               → [-1, -1]
```

## Constraints

- `values` has 0 to 400000 integers, each between -10^9 and 10^9; `target` is between -2 × 10^9 and 2 × 10^9.
- Time: O(n). Checking every pair is far too slow.
- Extra space: O(n).

## Hints

1. Standing at index `j`, which single value would you need to have seen earlier to finish a pair?
2. What could you store while scanning so that "have I seen that value, and where?" takes O(1)?
3. In `[3, 2, 4]` with target 6, what goes wrong if you record the current value before checking for its partner?
4. If a value appears more than once before `j`, which of its indices should you keep so that you return the smallest `i`?

## Explain-back

- Why does checking before recording stop an element from pairing with itself, while still allowing `[3, 3]` with target 6?
- Why does your single scan return the pair with the smallest `j`, and what makes it pick the smallest `i` for that `j`?
- What are the time and extra space complexity of your solution, and of the nested-loop version? When might the nested loops still be reasonable?
- Could you use a plain object `{}` instead of a `Map` here? What happens to the number keys, and what about a key like `"constructor"`?
