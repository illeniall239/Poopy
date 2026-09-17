# Merge sort

Topic: 10. Sorting
Difficulty: 2 of 3

## Problem

A leaderboard service receives scores in arbitrary order and needs them sorted, and you want to see exactly how an O(n log n) sort does it.

Write `mergeSort(nums: number[]): number[]` that returns a **new** array holding the same numbers as `nums`, in ascending numeric order.

- Use merge sort: split the array in half, sort each half, then merge the two sorted halves into one.
- Don't change `nums`, and don't use the built-in `sort` or `toSorted`.
- Duplicates are kept: the result has exactly as many elements as `nums`.
- Numbers are compared as numbers, so `9` comes before `10`.

## Examples

```
mergeSort([5, 2, 9, 1, 5, 6])  → [1, 2, 5, 5, 6, 9]
mergeSort([10, 9, 100, 1])     → [1, 9, 10, 100]
mergeSort([-3, 0, -7, 4])      → [-7, -3, 0, 4]
mergeSort([])                  → []
```

## Constraints

- `nums` has 0 to 1000000 elements; each is a whole number from -1000000000 to 1000000000.
- Required: O(n log n) time in every case and O(n) extra space.
- The large test sorts 300000 numbers in shuffled order, so O(n²) sorts such as insertion sort or selection sort are too slow.

## Hints

1. Suppose someone hands you two sorted piles of cards, `[1, 5, 9]` and `[2, 3, 10]`. How do you combine them into one sorted pile looking only at the top card of each?
2. When one pile runs out during that merge, what do you do with the cards still left in the other pile?
3. What is the smallest array that is already sorted without doing anything? That's your base case.
4. Split, sort both halves, merge: how many times can you halve n before reaching size 1, and how much work does merging all the arrays at one level take in total?

## Explain-back

- Why is merge sort O(n log n) in the best, average and worst case? Describe the levels of splitting and the work per level.
- Where does the O(n) extra space come from, and how much does the recursion stack add?
- What happens to the result if your merge forgets the leftover elements of one half? Which test would catch it?
- Merge sort is stable. What does that mean, and which comparison in your merge (`<` or `<=`) keeps it stable?
