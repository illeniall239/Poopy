# Quicksort in place

Topic: 10. Sorting
Difficulty: 3 of 3

## Problem

A sensor logger stores millions of readings in one big array and can't afford a second copy of it. It needs the readings sorted where they are.

Write `quickSort(nums: number[]): void` that sorts `nums` **in place** into ascending numeric order and returns nothing.

- Use quicksort: pick a pivot, rearrange the elements so smaller values come before the pivot and larger values after it, then sort each side the same way.
- Don't create a copy of the array (no `slice`, spread, `filter` or `concat` of the elements), and don't use the built-in `sort` or `toSorted`.
- It must stay fast on input that is already sorted, sorted in reverse, or where every value is the same.

## Examples

```
const a = [5, 2, 9, 1, 5, 6];
quickSort(a);    // returns undefined
a                → [1, 2, 5, 5, 6, 9]

const b = [3, 3, 3];
quickSort(b);
b                → [3, 3, 3]
```

## Constraints

- `nums` has 0 to 1000000 elements; each is a whole number from -1000000000 to 1000000000.
- Required: O(n log n) expected time on every input, including sorted, reversed and all-equal arrays, and O(log n) expected extra space for the recursion.
- The large tests sort 200000 shuffled, sorted, reversed and all-equal numbers. Always using the first or last element as the pivot is O(n²) and overflows the call stack on sorted input, and a partition that sends every equal value to one side does the same on all-equal input.

## Hints

1. After one partition step, where is the pivot, and what do you know about every element to its left and to its right?
2. Try partitioning `[1, 2, 3, 4, 5]` with the first element as the pivot. How big are the two sides? What does that do to the depth of recursion? How could you choose the pivot so no fixed input is always bad?
3. Now try `[4, 4, 4, 4, 4]` with your partition. Where do the elements equal to the pivot go? What if you kept three regions: less than, equal to and greater than the pivot?
4. Your function sorts a range of the array, so it needs to know which range. Which two indices describe that range, and what are they for the first call?

## Explain-back

- Why is quicksort O(n log n) on average but O(n²) in the worst case? Describe an input and pivot rule that hits the worst case.
- How does your code handle an array where every value is equal, and why is that O(n) or O(n log n) rather than O(n²)?
- What extra space does your quicksort use? Where does the recursion stack come in?
- Quicksort is usually not stable while merge sort is. When would that difference matter?
