# Sparse matrix

Topic: 3. Classes for building data structures
Difficulty: 2 of 3

## Problem

Many real matrices (road networks, "who follows whom", word counts per document) are huge but almost entirely zeros. Storing every cell wastes memory and time.

Write a class `SparseMatrix` that stores only the non-zero cells:

- `constructor(rows, cols)` creates a `rows` × `cols` matrix of zeros.
- `set(row, col, value)` sets that cell. Setting a cell to `0` removes it from storage.
- `get(row, col)` returns the cell's value, which is `0` for any cell that isn't stored.
- `nonZeroCount()` returns how many cells are currently stored.
- `multiplyVector(vector)` returns a new array of length `rows`, where entry `r` is the sum over every column `c` of `get(r, c) * vector[c]`. `vector` has length `cols`. Rows with no stored cells give `0`.

`set` and `get` must be O(1) on average. `multiplyVector` must take O(rows + nonZeroCount()) time: it must never loop over every cell of the matrix.

## Examples

```
const m = new SparseMatrix(2, 3);   // [[0, 0, 0],
m.set(0, 0, 1);                     //  [0, 0, 0]]
m.set(0, 2, 2);
m.set(1, 1, 3);                     // now [[1, 0, 2], [0, 3, 0]]
m.get(0, 1)                   → 0
m.nonZeroCount()              → 3
m.multiplyVector([4, 5, 6])   → [16, 15]     1·4 + 0·5 + 2·6, 0·4 + 3·5 + 0·6
m.set(0, 2, 0);
m.nonZeroCount()              → 2
```

## Constraints

- `1 <= rows, cols <= 200000`, so the full matrix can have 4 × 10^10 cells.
- At most 400000 cells are non-zero at once. Values and vector entries are integers between -1000 and 1000.
- Every `row` and `col` passed in is within bounds.

## Hints

1. A 200000 × 200000 matrix of numbers: how many bytes would a full 2-D array need? What is the most you actually need to store?
2. To multiply, you walk the stored cells rather than all cells. For each stored cell, which entry of the result does it contribute to, and what does it add?
3. How could you organise the stored cells so that `get` and `set` find a cell in O(1) on average? A `Map` keyed by something built from `row` and `col`, or one `Map` per row: what does each cost?
4. What must `set(row, col, 0)` do so that `nonZeroCount()` stays correct, both when the cell was stored and when it wasn't?

## Explain-back

- What are the time and space complexity of your `multiplyVector` and of your storage? Compare them with a full 2-D array.
- Why must `set(r, c, 0)` delete the cell rather than store a `0`? Which invariant would break otherwise?
- If you keyed a single `Map` by the string `` `${row},${col}` ``, what would that cost compared with numeric keys, and what goes wrong with `` `${row}${col}` ``?
- When is a full 2-D array the better choice, even though it uses more memory?
