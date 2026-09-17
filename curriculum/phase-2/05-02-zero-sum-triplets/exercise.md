# Zero-sum triplets

Topic: 5. Two pointers
Difficulty: 3 of 3

## Problem

Write `zeroSumTriplets(values: number[]): number[][]`.

Return every distinct triplet of values taken from three different positions of `values` whose sum is 0.

- Each triplet is an array of three numbers in non-decreasing order, such as `[-1, 0, 1]`.
- Two triplets that contain the same three numbers are the same triplet and must appear only once, however many times those numbers occur in `values`.
- Return the triplets sorted in lexicographic order: by their first number, then second, then third. Return `[]` when there is no triplet, including for fewer than three values.
- Don't change `values`.

## Examples

```
zeroSumTriplets([-1, 0, 1, 2, -1, -4])    → [[-1, -1, 2], [-1, 0, 1]]
zeroSumTriplets([0, 0, 0, 0])             → [[0, 0, 0]]
zeroSumTriplets([-2, 0, 1, 1, 2])         → [[-2, 0, 2], [-2, 1, 1]]
zeroSumTriplets([1, 2, -2, -1])           → []
zeroSumTriplets([])                       → []
```

## Constraints

- `values` has 0 to 5000 integers, each between -10^5 and 10^5.
- Time: O(n²). Trying every triplet is O(n³) and far too slow for 5000 values.
- Extra space: O(n) beyond the output (a sorted copy is fine).

## Hints

1. Fix one value `a`. What must the other two add up to, and which exercise from this Topic solves that in O(n) once the array is sorted?
2. Sorting first costs O(n log n). What does it buy you for the two-pointer part, and what does it buy you for producing the triplets in the required order?
3. In `[-1, -1, 0, 1, 2]`, fixing the first `-1` and fixing the second `-1` produce the same triplets. When should you skip a value, and what does "skip" mean for the inner pointers after a triplet is found?
4. Trace `[0, 0, 0, 0]` through your code. Does it report `[0, 0, 0]` exactly once?

## Explain-back

- Why does the output come out in lexicographic order without a final sort, given how you loop?
- Where exactly do you skip duplicates, and what goes wrong if you skip before the first triplet is found instead of after?
- What are the time and extra space complexity of your solution? Why doesn't the inner `while` loop make the total O(n³)?
- Could you solve this with a `Set` of seen values instead of two pointers? What would its complexity be, and how would you avoid duplicate triplets?
