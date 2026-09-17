# Binary search index

Topic: 8. Binary search
Difficulty: 1 of 3

## Problem

A phone book app stores user IDs in a sorted array and needs to find where an ID sits.

Write `binarySearch(sorted: number[], target: number): number`. `sorted` holds distinct whole numbers in strictly increasing order. Return the index of `target` in `sorted`, or `-1` if it isn't there.

Don't change `sorted`, and don't use `indexOf`, `includes`, `findIndex` or any other built-in search.

## Examples

```
binarySearch([1, 3, 5, 7, 9, 11], 7)   → 3
binarySearch([1, 3, 5, 7, 9, 11], 1)   → 0
binarySearch([1, 3, 5, 7, 9, 11], 4)   → -1
binarySearch([1, 3, 5, 7, 9, 11], 12)  → -1
binarySearch([], 5)                    → -1
```

## Constraints

- `sorted` has 0 to 1000000 elements; values and `target` are whole numbers from -2000000000 to 2000000000.
- Required: O(log n) time per call and O(1) extra space.
- The large test makes 100000 calls on an array of 1000000 values, so scanning the array is too slow.

## Hints

1. You look in the middle of the array and the value there is smaller than `target`. Which half can you now ignore completely, and why?
2. Use two variables for the part of the array that could still contain `target`. Decide right now: is `hi` the last index that might hold it, or one past it?
3. With your choice of `lo` and `hi`, what condition means "there is nothing left to search"? After looking at `mid`, what are the new `lo` and `hi`, so that `mid` is never looked at again?
4. Trace `[5]` with target `5`, and `[5]` with target `6`, step by step. Does your loop end in both cases?

## Explain-back

- State your loop invariant: what is always true about `lo`, `hi` and where `target` could be, at the start of every loop?
- Why is this O(log n)? About how many steps does it take for 1000000 elements?
- In Java, why can `(lo + hi) / 2` go wrong for very large arrays, and what do you write instead?
- What would happen if the array were not sorted? Give a small example where your code returns the wrong answer.
