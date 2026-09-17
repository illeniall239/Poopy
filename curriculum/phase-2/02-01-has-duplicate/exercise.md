# Has duplicate

Topic: 2. Big-O: time and space complexity
Difficulty: 1 of 3

## Problem

Write `hasDuplicate(values: number[]): boolean`. It returns `true` if some value appears at least twice in `values`, and `false` otherwise. An empty array and a single-element array have no duplicates.

Don't change `values`.

## Examples

```
hasDuplicate([1, 2, 3, 1])  → true
hasDuplicate([1, 2, 3])     → false
hasDuplicate([])            → false
hasDuplicate([7])           → false
```

## Constraints

- `values` has 0 to 400000 integers, each between -10^9 and 10^9.
- Time: O(n). Comparing every pair is far too slow for the largest inputs.
- Extra space: O(n) is allowed.

## Hints

1. Write the pair-comparing version in your head. How many comparisons does it make for 400000 values, and how long would that take at about 10^8 simple steps per second?
2. As you read the values left to right, what would you need to remember to know instantly whether the current value came up before?
3. Which built-in collection answers "have I seen this?" in O(1) on average, and which array method looks like it does but is O(n)?
4. Could you stop before reaching the end of the array? When?

## Explain-back

- What are the time and the extra space complexity of your solution? Does the input array itself count as extra space?
- Why is a loop that calls `values.includes(...)` or `indexOf` inside it O(n²), even though it looks like one loop?
- Sorting a copy first and checking neighbours also works. What is its complexity, and when might you still prefer it?
- For n = 400000, roughly how many steps do the O(n²) and O(n) approaches take? Is O(2n) meaningfully worse than O(n) in Big-O terms?
