# Pipeline and cross-validation

Topic: 20. The practical workflow: a scikit-learn-style capstone
Difficulty: 3 of 3

## Problem

Preprocessing is part of the model. If a scaler learns its mean and standard deviation from all the rows before cross-validation, every validation fold has already leaked into training. Write a small `Pipeline` class and a `cross_val_score` function with NumPy (allowed) that make the leak impossible.

The pieces are passed in, so any preprocessing and any model work:

- a **step** has `fit(X)` (learns from `X`; its return value is ignored) and `transform(X)` (returns a new array);
- a **model** has `fit(X, y)` and `predict(X)` (returns one prediction per row).

Write:

- `Pipeline(steps: list, model)` stores the steps (in order) and the model.
  - `fit(self, X: np.ndarray, y: np.ndarray) -> Pipeline`: for each step in order, call `step.fit(X)` and then `X = step.transform(X)`, so each step learns from the output of the one before. Then call `model.fit(X, y)` on the fully transformed `X`. Return `self`.
  - `predict(self, X: np.ndarray) -> np.ndarray`: pass `X` through every step's `transform` (never `fit`), then return `model.predict` of the result.
- `cross_val_score(pipeline: Pipeline, X: np.ndarray, y: np.ndarray, folds: list, metric) -> list[float]`: `folds` is a list of `(train_idx, val_idx)` pairs of row-index lists. For each fold, in order: fit the whole pipeline on the training rows only, predict the validation rows, and score them with `metric(y_val, predictions)`. Return the list of per-fold scores as floats. The same pipeline object is refitted for each fold. Raise `ValueError` if `folds` is empty.

## Examples

```
X = np.arange(6.0)[:, None];  y = np.array([0, 2, 4, 6, 8, 10.0])
folds = [([0, 1, 2, 3], [4, 5]), ([2, 3, 4, 5], [0, 1])]
mse = lambda t, p: float(np.mean((t - p) ** 2))
cross_val_score(Pipeline([], MeanModel()), X, y, folds, mse)    → [37.0, 37.0]
    fold 1: mean of 0, 2, 4, 6 is 3, so ((8 - 3)² + (10 - 3)²) / 2 = 37
Pipeline([StandardScaler()], KNNRegressor(3))                   the scaler is refitted inside every fold
Pipeline([scaler_prefitted_on_all_rows], KNNRegressor(3))       leaks, and scores differently
cross_val_score(pipeline, X, y, [], mse)                         → ValueError
```

(`MeanModel` predicts the mean of its training targets; `StandardScaler` and `KNNRegressor` are defined in the test.)

## Constraints

- NumPy allowed; no scikit-learn in the solution.
- The tests use up to 120 rows and 3 folds.
- Scores within `1e-9` of fitting each fold by hand.

## Hints

1. In `Pipeline.fit`, what array does the second step learn from: the raw `X` or the first step's output?
2. Why must `predict` call only `transform`? What would a scaler fitted on the validation rows do to the score?
3. In `cross_val_score`, at which exact moment may the pipeline see a row, and which rows is that?
4. A scaler fitted on all rows has seen the validation fold's mean and spread. How would you build a test that shows the score changes?

## Explain-back

- Why does a scaler fitted once on the full dataset leak information, even though it never sees the labels?
- You save only the trained model to disk, not the scaler. What goes wrong in production?
- Name the scikit-learn objects that do what `Pipeline`, `cross_val_score` and a grid search around them do.
- You tuned hyperparameters with this cross-validation and then scored the test set twice with different models. Why is neither test score an honest estimate any more?
