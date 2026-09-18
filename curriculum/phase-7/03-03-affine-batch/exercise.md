# Affine batch

Topic: 3. Matrices, matrix multiplication and broadcasting
Difficulty: 2 of 3

## Problem

A linear layer maps a batch of examples `X` (shape `(n, d)`, one example per row) to outputs `XW + b`, where `W` is `(d, k)` and `b` is `(k,)`. Write it twice:

- `affine_lists(X: list[list[float]], W: list[list[float]], b: list[float]) -> list[list[float]]` — pure Python over lists of rows. Row `i` of the result is `X[i] @ W + b`: `k` dot products of `X[i]` with the columns of `W`, plus the bias.
- `affine_numpy(X: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray` — the same with `@` and broadcasting, no Python loops, returning shape `(n, k)`.

Both raise `ValueError` when `X` has a different number of columns than `W` has rows, or when `b` does not have exactly `k` entries. `affine_numpy` must also raise `ValueError` if `b` is not 1-D: a `(k, 1)` bias would silently broadcast into something else.

`affine_lists` allows no NumPy; `affine_numpy` requires it.

## Examples

```
X = [[1, 2], [3, 4], [5, 6]]        (3, 2)
W = [[1, 0, -1], [2, 1, 0]]         (2, 3)
b = [10, 20, 30]                    (3,)
affine_lists(X, W, b)  → [[15, 22, 29], [21, 24, 27], [27, 26, 25]]
affine_numpy(np.array(X), np.array(W), np.array(b))  → the same as an array of shape (3, 3)

affine_lists([[1, 2, 3]], W, b)      → ValueError   X has 3 columns, W has 2 rows
affine_numpy(X, W, np.array([[10], [20], [30]]))  → ValueError   b is (3, 1)
```

## Constraints

- `n`, `d`, `k` up to 200; the list version may be a straightforward triple loop.
- The two versions agree with each other and with NumPy within `1e-9`.
- Neither function changes its inputs.

## Hints

1. For one example row `x` and one output column `j`, which entries of `W` are involved and which single entry of `b` is added?
2. In the list version, how do you get column `j` of `W` when `W` is stored as rows?
3. In NumPy, `X @ W` has shape `(n, k)` and `b` has shape `(k,)`. Line the shapes up from the right: why does `+ b` add the bias to every row without a loop?
4. Which shape check catches a `(k, 1)` bias before broadcasting turns `(n, k) + (k, 1)` into something surprising?

## Explain-back

- Describe `XW + b` in words as "one dot product per ..." and say what each row and each column of the result means.
- If `b` were shaped `(k, 1)` and `n == k`, what shape would `X @ W + b` have and why would no error be raised? Why is that worse than an exception?
- Why does the NumPy version not copy `b` n times, and how would you check that claim?
- How many multiplications does `affine_numpy` do for a batch of 64 examples with 784 inputs and 256 outputs? Which of `n`, `d`, `k` would you shrink to halve the work?
