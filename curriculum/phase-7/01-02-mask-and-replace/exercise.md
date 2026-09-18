# Mask and replace

Topic: 1. NumPy arrays and vectorization
Difficulty: 2 of 3

## Problem

Write `replace_outliers(x: np.ndarray, k: float) -> np.ndarray`.

`x` is a 2-D float array with one column per feature. A value is an outlier when its distance from its column's mean is strictly more than `k` times that column's population standard deviation (`ddof=0`). Return a new array in which every outlier is replaced by the median of its column, where the mean, standard deviation and median are all computed on the original column, before any replacement.

Use a boolean mask to select and assign. No Python loops over rows, columns or elements. `x` must not be modified.

NumPy is allowed (and expected).

## Examples

```
x = np.array([[1.0, 100.0],
              [2.0, 101.0],
              [3.0, 102.0],
              [4.0, 103.0],
              [50.0, 104.0]])
replace_outliers(x, 1.5)
→ array([[  1., 100.],
         [  2., 101.],
         [  3., 102.],
         [  4., 103.],
         [  3., 104.]])      50.0 was > 1.5 std from its column mean; column 1 is untouched

replace_outliers(np.array([[1.0], [1.0], [1.0]]), 2.0)  → array([[1.], [1.], [1.]])   std 0, nothing is an outlier
```

## Constraints

- `x` has at least one row and one column; `k >= 0`.
- The result has the same shape and dtype as `x` and must equal a straightforward loop version within `1e-9`.
- Values exactly `k` standard deviations away are not outliers.

## Hints

1. `x - x.mean(axis=0)` works even though the shapes are `(n, m)` and `(m,)`. Why, and what shape is the result?
2. How do you build one boolean array of shape `(n, m)` that is `True` exactly at the outlier positions?
3. You need the median of the *column* each outlier sits in. If `medians` has shape `(m,)`, what shape does `np.broadcast_to(medians, x.shape)` have, and how can a mask pick from it?
4. If you write `result = x` and then assign through the mask, what happens to the caller's array? What call gives you a separate copy first?

## Explain-back

- Why does `x[mask] = value` change the array while `y = x[mask]` gives you a copy? What is the difference between fancy indexing on the right and on the left of `=`?
- Why does `x[0:2]` give a view but `x[[0, 1]]` a copy? Show a one-line experiment that proves it.
- Why must the median be computed before the replacement rather than after? Give a tiny column where it matters.
- Compare two float arrays `a` and `b` that should be equal. Why is `(a == b).all()` risky and what does `np.allclose` do differently?
