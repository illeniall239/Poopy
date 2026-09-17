# Merge intervals

Topic: 17. Intervals and greedy algorithms
Difficulty: 2 of 3

## Problem

A calendar holds busy periods as closed intervals `[start, end]` with `start <= end`, in no particular order and possibly overlapping. To show the free time, the busy periods have to be merged.

Write `mergeIntervals(intervals: [number, number][]): [number, number][]`. Return the smallest set of intervals that covers exactly the same points, sorted by `start`.

- Two intervals overlap when they share at least one point: `[1, 4]` and `[4, 5]` overlap at 4 and merge into `[1, 5]`. `[1, 3]` and `[4, 5]` do not overlap.
- An interval fully inside another disappears into it.
- Return new arrays. Don't change `intervals` or any of its pairs, and don't return the input pairs themselves.
- An empty input gives `[]`.

## Examples

```
mergeIntervals([[1, 3], [2, 6], [8, 10], [15, 18]])   → [[1, 6], [8, 10], [15, 18]]
mergeIntervals([[1, 4], [4, 5]])                      → [[1, 5]]
mergeIntervals([[8, 10], [1, 3], [2, 6]])             → [[1, 6], [8, 10]]
mergeIntervals([[1, 10], [2, 3], [4, 5]])             → [[1, 10]]
mergeIntervals([])                                    → []
```

## Constraints

- `intervals` has 0 to 400000 pairs; each bound is an integer between -10^9 and 10^9, with `start <= end`.
- Time: O(n log n). Comparing every interval with every other is far too slow.
- Extra space: O(n) for the result and the sorted copy.

## Hints

1. Take `[[8, 10], [1, 3], [2, 6]]`. If you first put the intervals in order of `start`, which neighbours could possibly overlap? Which could not?
2. Walking through the sorted intervals, you keep a "current" merged interval. When the next interval overlaps it, which of the two `end` values should the current interval keep? Try `[[1, 10], [2, 3]]`.
3. What decides whether the next interval joins the current one or starts a new one? Write that test with `<=` or `<` and check it on `[[1, 4], [4, 5]]`.
4. How do you sort without reordering the caller's array, and how do you make sure the pairs you return are not the caller's pairs?

## Explain-back

- Why does sorting by `start` make a single left-to-right pass enough? What input breaks the pass if you skip the sort?
- Why is the answer one merged interval for `[[1, 10], [2, 3], [4, 5]]`, and what bug returns `[[1, 3], [4, 5]]` or `[[1, 5]]` instead?
- What are the time and space complexity of your solution, and which step dominates?
- If the intervals were half-open, `[start, end)`, would `[1, 4]` and `[4, 5]` still merge? Which single character of your code changes?
