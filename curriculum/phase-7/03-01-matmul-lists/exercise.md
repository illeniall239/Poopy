# Matmul on lists

Topic: 3. Matrices, matrix multiplication and broadcasting
Difficulty: 1 of 3

## Problem

Write two functions over matrices given as `list[list[float]]` (a list of rows, every row the same length), in pure Python (no NumPy):

- `matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]` — the matrix product. If `a` is `m×n` and `b` is `n×p`, the result is `m×p` and entry `(i, j)` is the dot product of row `i` of `a` with column `j` of `b`. Raise `ValueError` when the inner dimensions differ.
- `transpose(a: list[list[float]]) -> list[list[float]]` — the `n×m` matrix whose entry `(j, i)` is `a[i][j]`.

Neither function may modify its inputs.

## Examples

```
matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]])   → [[19, 22], [43, 50]]
matmul([[1, 2, 3]], [[1], [2], [3]])          → [[14]]          (1×3)(3×1) → 1×1
matmul([[1], [2], [3]], [[1, 2, 3]])          → [[1, 2, 3], [2, 4, 6], [3, 6, 9]]   (3×1)(1×3) → 3×3
matmul([[1, 2]], [[1, 2]])                    → ValueError      (1×2)(1×2): 2 ≠ 1
transpose([[1, 2, 3], [4, 5, 6]])             → [[1, 4], [2, 5], [3, 6]]
```

## Constraints

- Dimensions up to 60×60; the straightforward triple loop is fine.
- Results must match `numpy.matmul` and `.T` within `1e-9`.
- Every entry of the result is a `float`.

## Hints

1. For the result entry at row `i`, column `j`, which row of `a` and which column of `b` are involved, and how many products are summed?
2. `b` is stored as rows. What is the easiest way to get hold of column `j` of `b`? Could `transpose` help `matmul`?
3. Check `matmul([[1, 2]], [[1, 2]])` by hand. Which two numbers must be equal for the sum to be well defined?
4. What are the dimensions of the result, and how do you build a nested list of that size without every row being the same list object?

## Explain-back

- Why is `(3×1)(1×3)` a `3×3` matrix but `(1×3)(3×1)` a single number? What does each tell you about the row and column vectors?
- Is `matmul(a, b)` equal to `matmul(b, a)`? Give a `2×2` counterexample and explain why the shapes alone can rule it out for non-square matrices.
- How many multiplications does `matmul` do for `m×n` times `n×p`? For a batch of 1 000 examples with 784 features into 10 outputs, what is the count?
- If `X` holds one example per row and `W` has one column per output, what does row `i` of `X @ W` represent, and what does column `j` of `W` represent?
