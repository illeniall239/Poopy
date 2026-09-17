# Top k frequent values

Topic: 4. Arrays and hashing
Difficulty: 2 of 3

## Problem

Write `topKFrequent(values: number[], k: number): number[]`.

Return the `k` values that occur most often in `values`, each value once. Order the result from most to least frequent. When values occur equally often, the one whose **first occurrence** in `values` comes earlier goes first.

Do it in better than O(n log n) time: O(n) is possible. Don't change `values`.

## Examples

```
topKFrequent([1, 1, 1, 2, 2, 3], 2)        → [1, 2]
topKFrequent([9, 4, 4, 9, 1], 2)           → [9, 4]      9 and 4 both occur twice; 9 appears first
topKFrequent([3, 1, 1, 3, 2, 2, 2], 3)     → [2, 3, 1]
topKFrequent([5, 3, 8, 1], 3)              → [5, 3, 8]
```

## Constraints

- `values` has 1 to 400000 integers, each between -10^9 and 10^9.
- `1 <= k <=` the number of distinct values.
- Time: O(n). Counting by searching a list of values seen so far is far too slow when there are many distinct values.

## Hints

1. What do you need to know about every distinct value before you can pick the top k? Which structure builds that in one pass?
2. Sorting the distinct values by count would work. What does that cost, and why is it not O(n)?
3. A count can never be larger than `values.length`. How could you use the count itself as an array index to group values with the same count?
4. How do you make values with the same count come out in order of first appearance? Does the order you walk your counts in already give you that?

## Explain-back

- What are the time and extra space complexity of your solution? Where exactly would sorting add a log factor?
- Why can you use counts as array indices here, and why would that fail for "sort these values by size"?
- How did you guarantee the tie order? Would it still hold if you had used a plain object `{}` keyed by the values, given how objects order integer-like keys?
- For k = 1, what simpler O(n) approach is there, and why doesn't it extend nicely to general k?
