# Count queen placements

Topic: 14. Backtracking
Difficulty: 3 of 3

## Problem

A queen on a chessboard attacks every square in its row, its column and both of its diagonals, any distance away.

Write `countQueens(n)` that returns how many different ways there are to place `n` queens on an `n × n` board so that no two queens attack each other. Two placements are different if any square holds a queen in one and not in the other; placements that are rotations or reflections of each other still count separately.

## Examples

```
countQueens(1)  → 1
countQueens(2)  → 0
countQueens(4)  → 2
countQueens(8)  → 92
```

## Constraints

- 1 ≤ n ≤ 12.
- The tests include n = 12 (14 200 placements). Trying every arrangement of queens and checking it afterwards cannot finish in time; you need to prune as you place, and each "is this square safe?" check should be O(1).

## Hints

1. Can two queens ever share a row? What does that tell you about how many queens go in each row, and what the choice at each step of your search is?
2. Once you have placed queens in the first few rows, what must be true of a square in the next row before you put a queen there? When should you give up on a branch?
3. All squares on one "down-right" diagonal share something about `row` and `col`. What stays the same along it? What stays the same along an "up-right" diagonal?
4. If you keep a record of which columns and diagonals are already taken, what must you do to that record after exploring a choice and before trying the next column?

## Explain-back

- Why do you only choose a column for each row, instead of choosing any square on the board? How much does that shrink the search?
- How do you check in O(1) whether a square is attacked? What happens to your sets or arrays when you back out of a choice, and why?
- What is the rough upper bound on the running time (think about n choices, then fewer, then fewer)? How much memory does your search use?
- Where exactly does your code prune, and what would the running time look like without pruning?
