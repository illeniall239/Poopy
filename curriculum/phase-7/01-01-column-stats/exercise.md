# Column statistics

Topic: 1. NumPy arrays and vectorization
Difficulty: 1 of 3

## Problem

Write `column_stats(x: np.ndarray) -> dict[str, np.ndarray]`.

`x` is a 2-D float array with shape `(n_rows, n_cols)`: one row per example, one column per feature. Return a dict with the keys `"mean"`, `"std"`, `"min"` and `"max"`. Each value is a 1-D array of length `n_cols` holding that statistic for every column. `"std"` is the population standard deviation (`ddof=0`).

Use one NumPy reduction per statistic. No Python `for`/`while` loops and no comprehensions over rows or columns. Do not change `x`.

NumPy is allowed (and expected).

## Examples

```
x = np.array([[1.0, 10.0],
              [3.0, 30.0],
              [5.0, 50.0]])
column_stats(x)["mean"]  → array([ 3., 30.])
column_stats(x)["std"]   → array([1.63299316, 16.32993162])
column_stats(x)["min"]   → array([ 1., 10.])
column_stats(x)["max"]   → array([ 5., 50.])

column_stats(np.array([[7.0, -2.0]]))["std"]  → array([0., 0.])
```

## Constraints

- `x` has at least one row and one column; up to 200 000 × 50 must finish in well under a second.
- Every returned array has shape `(n_cols,)`, not `(1, n_cols)` or `(n_rows,)`.
- Results must match NumPy's own reductions within `1e-9`.

## Hints

1. `x.mean()` with no arguments gives one number. Which argument makes it give one number per column, and what does that argument actually collapse?
2. Print `x.mean(axis=0).shape` and `x.mean(axis=1).shape` for a 3×2 array. Which one is "per column"?
3. Do you need to reshape or transpose `x` at all, or does the axis argument already do the work?
4. `np.std` takes a `ddof` argument. What is its default, and does the problem ask for that default?

## Explain-back

- `axis=0` collapses rows and leaves one value per column. Why does "axis 0" not mean "along a row"? What does `x.sum(axis=1)` give?
- Why is one call to `x.mean(axis=0)` faster than a Python loop that averages each column? Where does the loop happen instead?
- Your function returns arrays of shape `(n_cols,)`. What would `keepdims=True` change, and when would you want that?
- If `x` were an `int8` array, what could go wrong inside `x.sum(axis=0)` in a language with fixed-width integers, and how does NumPy actually handle that case for `sum`?
