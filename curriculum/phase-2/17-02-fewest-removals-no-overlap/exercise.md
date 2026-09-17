# Fewest removals for non-overlapping intervals

Topic: 17. Intervals and greedy algorithms
Difficulty: 2 of 3

## Problem

A single meeting room has received a list of booking requests. Each request is an interval `[start, end]` with `start < end`. Requests that overlap cannot both be accepted. You want to reject as few requests as possible so that all the remaining ones fit in the room.

Write `fewestRemovals(intervals: [number, number][]): number`. It returns the smallest number of intervals to remove so that no two remaining intervals overlap.

- Two intervals overlap when they share more than a single point. `[1, 3]` and `[2, 4]` overlap; `[1, 2]` and `[2, 3]` do not, because one ends exactly where the other starts.
- Identical intervals overlap each other, so of three copies of `[1, 2]` two must go.
- An empty array or a single interval needs no removals: return `0`.
- Coordinates may be negative.
- Don't change the array you are given or the intervals inside it; the tests check.

## Examples

```
fewestRemovals([[1, 2], [2, 3], [3, 4], [1, 3]])   → 1     (remove [1, 3])
fewestRemovals([[1, 2], [1, 2], [1, 2]])           → 2
fewestRemovals([[1, 2], [2, 3]])                   → 0
fewestRemovals([[1, 10], [2, 3], [4, 5], [6, 7]])  → 1     (remove [1, 10], not the three short ones)
fewestRemovals([])                                 → 0
```

## Constraints

- 0 ≤ `intervals.length` ≤ 200 000; -10⁹ ≤ `start` < `end` ≤ 10⁹.
- Required: O(n log n) time and O(n) extra space.
- The large test has 200 000 intervals (100 000 in Python), too many for anything O(n²).

## Hints

1. Turn the question around: keep as many intervals as you can, and the answer is the total minus that. If you choose intervals one at a time from left to right, which property of the interval you keep leaves the most room for the ones after it?
2. Sorting by start and always keeping the earliest-starting interval gives the wrong answer on the fourth example. Why? Which key should you sort by instead?
3. Once sorted, walk through the intervals while tracking a single number: the end of the last interval you kept. When does the next interval get kept, and when does it get counted as removed? Is a start equal to that end a conflict?
4. Suppose some best possible set keeps a different first interval than yours. Could you swap it for the one that ends earliest without breaking anything? What does that say about your first choice, and every choice after it?

## Explain-back

- Why is "keep the interval that ends earliest" always safe? Explain the swap argument in your own words.
- Give a small input where sorting by start and keeping the earliest-starting interval gives the wrong answer, and show what your solution does on it.
- What are the time and space complexity? Which step dominates, and how do you avoid mutating the input?
- How would the code change if touching intervals such as `[1, 2]` and `[2, 3]` counted as overlapping?
