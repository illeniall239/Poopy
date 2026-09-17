# Count islands

Topic: 15. Graphs
Difficulty: 2 of 3

## Problem

A map is given as `grid`, an array of strings. Every string is one row and all rows have the same length. Each character is either `"1"` (land) or `"0"` (water).

Two land cells belong to the same island if you can walk from one to the other stepping only on land, moving up, down, left or right one cell at a time. Diagonal steps do not count. Everything outside the grid is water.

Write `countIslands(grid)` that returns the number of islands. An empty grid (`[]`) has 0 islands.

## Examples

```
countIslands([
  "11000",
  "11000",
  "00100",
  "00011",
])  → 3

countIslands(["101", "010", "101"])  → 5    (diagonal cells are not connected)
countIslands(["000"])                → 0
```

## Constraints

- 0 ≤ rows ≤ 1000; 1 ≤ columns ≤ 1000.
- O(rows × columns) time. The tests include a 1000 × 1000 grid (500 × 500 in Python) with hundreds of thousands of islands.
- The largest single island in the tests has 625 cells, so recursion is fine here, but think about what would happen on a grid that is all land.

## Hints

1. Think of each land cell as a node in a graph. Which cells are its neighbours, and how do you make sure you never read outside the grid?
2. Suppose you scan the grid row by row and land on a `"1"`. How can you tell whether it belongs to an island you have already counted?
3. When you find land that is not yet part of a counted island, what should you do to every cell of that island right away so it is never counted again?
4. Strings can't be changed in place. Where will you record which cells you have visited, and at which moment should a cell be recorded so it is never added twice?

## Explain-back

- Why is the total time O(rows × columns) even though you start a search from inside a loop over every cell?
- How much extra space does your solution use, counting the visited record and the recursion stack or explicit stack/queue? What is the worst case?
- Where do you check the grid bounds, and what goes wrong if you index first and check afterwards?
- What would happen without marking cells visited? Would recursive DFS on a 1000 × 1000 all-land grid be safe, and what would you use instead?
