# Range sum queries

Topic: 2. Big-O: time and space complexity
Difficulty: 2 of 3

## Problem

Write `rangeSums(values: number[], queries: [number, number][]): number[]`.

Each query `[i, j]` asks for `values[i] + values[i + 1] + ... + values[j]`, with both ends included. Return one sum per query, in the same order as `queries`. No queries gives `[]`. Don't change `values` or `queries`.

## Examples

```
rangeSums([3, -2, 5, 1, 4], [[0, 2], [1, 3], [2, 4]])  → [6, 4, 10]
rangeSums([3, -2, 5, 1, 4], [[3, 3], [0, 4]])          → [1, 11]
rangeSums([7], [])                                     → []
```

## Constraints

- `values` has 1 to 1000000 integers, each between -10^6 and 10^6.
- `queries` has 0 to 1000000 entries, and every query has `0 <= i <= j < values.length`.
- Time: O(n + q). Adding up each range separately is far too slow when there are many long queries.
- Extra space: O(n) besides the result.

## Hints

1. How much work does one query take if you add the range up directly? What if there are a million queries, each covering half the array?
2. If you knew the sum of everything before index 5 and the sum of everything up to index 9, how could you get the sum of indices 5 to 9 without a loop?
3. What one array, built in a single pass before answering any query, would give you those "sum so far" numbers?
4. Your query `[0, j]` needs "the sum of everything before index 0". How can you set up your array so that isn't a special case?

## Explain-back

- What does each entry of your helper array mean, in words? Why is it one element longer than `values` (or why isn't it)?
- What are the time and extra space complexity of your solution? How does that compare with the direct approach for n = q = 10^6?
- If the values could change between queries, what would stop working, and what would an update cost?
- In Java the sums can exceed the range of an `int`. Which numbers overflow first, and what type holds them safely?
