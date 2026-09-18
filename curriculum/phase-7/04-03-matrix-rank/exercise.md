# Matrix rank

Topic: 4. Linear systems, inverse, determinant
Difficulty: 3 of 3

## Problem

Write two functions over a matrix given as a list of rows (any shape `m×n`), in pure Python (no NumPy):

- `matrix_rank(a: list[list[float]], tol: float = 1e-9) -> int` — the number of linearly independent rows (equivalently columns). Reduce `a` to row echelon form with partial pivoting and count the pivots; a candidate pivot whose absolute value is at most `tol` counts as zero and its column is skipped (move to the next column, staying on the same row).
- `is_singular(a: list[list[float]], tol: float = 1e-9) -> bool` — `True` when a square matrix has rank below `n`. Raise `ValueError` if `a` is not square.

Do not modify the input. The tolerance matters: a column that equals another column plus `1e-14` noise is dependent for any sensible purpose, and the test checks that.

## Examples

```
matrix_rank([[1, 0], [0, 1]])                   → 2
matrix_rank([[1, 2], [2, 4]])                   → 1
matrix_rank([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  → 2
matrix_rank([[1, 2, 1], [3, 4, 3], [5, 6, 5]])  → 2      third column duplicates the first
matrix_rank([[1, 2, 3], [4, 5, 6]])             → 2      2×3
matrix_rank([[0, 0], [0, 0]])                   → 0
is_singular([[1, 2], [2, 4]])                   → True
is_singular([[1, 2, 3]])                        → ValueError
```

## Constraints

- Up to 40 rows and 40 columns.
- Must agree with `numpy.linalg.matrix_rank` on every test matrix, including a `20×5` matrix whose fifth column is the sum of the others plus noise of size `1e-13` (rank 4 at `tol=1e-9`, rank 5 at `tol=0`).
- `tol` is compared against absolute values after pivoting, so scale your test matrices sensibly (entries around 1).

## Hints

1. In a square, full-rank matrix elimination produces `n` non-zero pivots. What happens to a column when every candidate pivot is (nearly) zero, and what should the algorithm do next?
2. Keep two counters: the current pivot row and the current column. Which one advances on a skipped column?
3. A duplicated column is not obvious from the rows. After eliminating on the first column, what does the third column of `[[1, 2, 1], [3, 4, 3], [5, 6, 5]]` look like?
4. Why compare the pivot against `tol` rather than against `0`? What float would `1 - (1/3) * 3` give?

## Explain-back

- A dataset has a `price_usd` column and a `price_cents` column. What is the rank of the feature matrix relative to its column count, and what happens when least squares solves `XᵀX w = Xᵀy`?
- Rank is the same whether you count independent rows or independent columns. What does that say about a `100×5` feature matrix's maximum rank?
- `matrix_rank` with `tol=0` on floating-point data gives full rank almost always. Why, and what does that tell you about "exactly singular" in practice?
- How is `is_singular` related to `determinant` from the earlier exercise? Which is the more reliable check for a `30×30` matrix with entries around `0.01`, and why?
