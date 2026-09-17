# Widest container

Topic: 5. Two pointers
Difficulty: 2 of 3

## Problem

`heights[i]` is the height of a vertical wall standing at position `i` along a line; neighbouring positions are 1 apart. Pick two walls `i < j` and fill the space between them with water: the water rises to the shorter wall, so the area held is `(j - i) * min(heights[i], heights[j])`. Walls in between don't matter.

Write `widestContainer(heights: number[]): number`. Return the largest area any two walls can hold. With fewer than two walls, return 0.

Don't change `heights`.

## Examples

```
widestContainer([1, 8, 6, 2, 5, 4, 8, 3, 7])   → 49      walls at 1 and 8: 7 * min(8, 7)
widestContainer([4, 3, 2, 1, 4])               → 16
widestContainer([1, 2, 1])                     → 2
widestContainer([2, 3, 4, 5, 18, 17, 6])       → 17
widestContainer([5])                           → 0
```

## Constraints

- `heights` has 0 to 400000 integers, each between 0 and 10^4.
- Time: O(n). Checking every pair of walls is far too slow.
- Extra space: O(1).

## Hints

1. Start with the two outermost walls: that is the widest container possible. Every other container is narrower, so how could it still hold more?
2. Say the left wall is the shorter one. Consider every container that keeps this left wall and uses some wall further in on the right. Can any of them beat the one you just measured? What does that tell you about which pointer to move?
3. What if the two walls are the same height? Does it matter which pointer you move?
4. Trace `[1, 2, 1]` and `[5]` through your loop. When does the loop stop, and what is returned for a single wall?

## Explain-back

- State the argument that moving the shorter wall inward never skips the best container. What would go wrong if you moved the taller wall instead?
- Why is the answer for two equal outer walls safe whichever pointer you move?
- What are the time and extra space complexity of your solution, and of the nested-loop version?
- Is this a greedy algorithm, an exhaustive search, or something else? Which containers does it never even look at?
