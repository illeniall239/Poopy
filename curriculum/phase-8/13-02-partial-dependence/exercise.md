# Partial dependence

Topic: 13. Interpretability for tabular models
Difficulty: 2 of 3

## Problem

A partial-dependence curve shows how a trained model's average prediction moves as one feature sweeps a range, with every other feature left as it really is in the data. Write it with NumPy:

```
partial_dependence(predict, X: np.ndarray, feature: int, grid: list[float]) -> np.ndarray
```

- `predict` maps an `(n, d)` array to `n` predictions (an already-trained model).
- For each value `g` in `grid`, in order: copy `X`, set column `feature` of **every** row of the copy to `g`, and take the mean of `predict(copy)`.
- Return a float array with one average per grid value (shape `(len(grid),)`; an empty grid gives an empty array).

This is the average of the predictions, not the prediction at the average row: for a model that is not linear the two differ. Do not modify `X`. Raise `ValueError` if `X` is not a non-empty 2-D array or `feature` is not a valid column index (`0 <= feature < d`).

## Examples

```
X = np.array([[0.0, 1.0], [0.0, 3.0]])
partial_dependence(lambda A: 2 * A[:, 0] + A[:, 1], X, 0, [0.0, 1.0, 2.0])  → [2.0, 4.0, 6.0]
partial_dependence(lambda A: A[:, 0] * A[:, 1] ** 2, X, 0, [1.0])          → [5.0]    mean of 1·1 and 1·9
    (the prediction at the mean row would be 1 · 2² = 4.0)
partial_dependence(lambda A: A[:, 0], X, 2, [1.0])                          → ValueError
```

## Constraints

- NumPy allowed; no scikit-learn.
- `n` ≤ 5 000, `len(grid)` ≤ 100: one `predict` call per grid value.
- Results within `1e-9` of the exact values.

## Hints

1. For one grid value, which rows do you change, which column, and what stays exactly as it was in the data?
2. Why average the model's outputs over all rows rather than plug the average row into the model once? Try it on `x0 · x1²` with `x1` in `{1, 3}`.
3. For a linear model `w0·x0 + w1·x1 + b`, what shape must the curve for feature 0 have, and what is its slope?
4. If you edit the column in `X` directly for the first grid value, what does the second grid value's computation see?

## Explain-back

- Your curve for "age" rises steeply between 90 and 100, but only three training rows have an age above 80. How much should you trust that part of the curve, and why?
- Two features are strongly correlated (house area and number of rooms). Why can partial dependence on one of them average over impossible rows?
- A partial-dependence curve is flat. Does that prove the model ignores the feature? Think of `x0 · x1` with `x1` centred at zero.
- What is the difference between this global curve and a local explanation of one prediction?
