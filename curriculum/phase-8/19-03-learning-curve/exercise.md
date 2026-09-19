# Learning curve

Topic: 19. Error analysis and project strategy
Difficulty: 2 of 3

## Problem

Before paying for more data, check whether more data would help. A learning curve trains the same model on growing training sets and plots training and validation error against the training-set size. Write two functions with NumPy (allowed):

- `learning_curve(fit, predict, X: np.ndarray, y: np.ndarray, sizes: list[int], folds: list) -> list[tuple[int, float, float]]`
  - `fit(X_sub, y_sub)` trains a model and returns it; `predict(model, X_rows)` returns one prediction per row. Both are passed in, so the curve works for any model.
  - `folds` is a list of `(train_idx, val_idx)` pairs of row-index lists.
  - For each size `s` in `sizes`, and for each fold: fit on the first `s` indices of that fold's `train_idx` (in the order given), then compute the training error as the mean squared error on those same `s` rows and the validation error as the mean squared error on all of `val_idx`.
  - Return one `(s, mean training error, mean validation error)` tuple per size, in the order of `sizes`, each mean taken over the folds.
  - Raise `ValueError` if `sizes` or `folds` is empty, or any size is below 1 or above the length of the shortest `train_idx`.
- `more_data_helps(curve: list[tuple[int, float, float]], tol: float = 1e-3) -> bool` reads a curve from `learning_curve`. With `gap = validation error - training error` at each size, return `True` only when the gap at the largest size is still open (`> tol`) and still closing (the gap at the second-to-last size minus the last gap is `> tol`). Raise `ValueError` if the curve has fewer than two points.

## Examples

```
X = np.arange(6)[:, None];  y = np.array([0, 2, 4, 6, 8, 10.0])
fit = lambda X, y: y.mean();  predict = lambda m, X: np.full(len(X), m)
learning_curve(fit, predict, X, y, [2, 4], [([0, 1, 2, 3], [4, 5])])
    → [(2, 1.0, 65.0), (4, 5.0, 37.0)]
more_data_helps([(10, 0.05, 0.60), (20, 0.08, 0.40), (40, 0.10, 0.30)])   → True    gaps 0.55, 0.32, 0.20
more_data_helps([(10, 0.10, 0.30), (20, 0.10, 0.30), (40, 0.10, 0.30)])   → False   the gap stopped closing
more_data_helps([(10, 0.10, 0.30)])                                       → ValueError
```

## Constraints

- NumPy allowed; no scikit-learn in the solution.
- The tests fit polynomials with `np.polyfit` on up to 600 rows; everything runs in well under a second.
- Errors within `1e-7`.

## Hints

1. At each size, which rows may the model see, and which rows is each of the two errors measured on?
2. Why is the training error measured on the `s` rows the model trained on, and not on the whole training fold?
3. As `s` grows, what usually happens to the training error and to the validation error of a model with high variance? Of one with high bias?
4. If validation error keeps falling but the gap has already shrunk to almost nothing, will more data of the same kind help much? What would?

## Explain-back

- The linear model on the sine data has high training error and almost no gap. Why would ten times more data not help, and what would?
- The degree-9 polynomial's gap was still closing at 60 rows. What does that predict for 600 rows, and how would you check it cheaply?
- Why do both errors come from the same folds and sizes, and what would go wrong if the validation rows could appear in the training subset?
- The gap is closing, but collecting data costs a lot. What other fixes for variance could you try first?
