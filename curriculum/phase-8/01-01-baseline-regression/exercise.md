# Baseline regression

Topic: 1. Framing a problem, baselines, and when not to use ML
Difficulty: 1 of 3

## Problem

Before any model, a regression task needs the number to beat. Write three pure-Python functions (no numpy):

- `mean_baseline(train_ys: list[float]) -> float` returns the mean of the training targets. This is the whole "model": it predicts that number for every row. Raise `ValueError` on an empty list.
- `mse(y_true: list[float], y_pred: list[float]) -> float` returns the mean squared error. Raise `ValueError` if the lengths differ or the lists are empty.
- `baseline_mse(train_ys: list[float], val_ys: list[float]) -> float` fits the baseline on `train_ys` only and returns its MSE on `val_ys`.

The validation targets must never influence the baseline's prediction.

## Examples

```
mean_baseline([1.0, 2.0, 3.0])            → 2.0
mse([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])     → 0.0
mse([1.0, 2.0], [2.0, 4.0])               → 2.5      ((1 + 4) / 2)
baseline_mse([1.0, 2.0, 3.0], [2.0, 4.0]) → 2.0      predicts 2.0 for both: (0 + 4) / 2
```

## Constraints

- Pure Python: `math` and `statistics` are allowed, numpy is not.
- Lists hold at most 100 000 floats.
- `baseline_mse` is O(n + m).

## Hints

1. If you may predict only one number for every row, which number makes the squared error smallest on the training data?
2. What is the difference between the error you would get on the training rows and the error you get on rows the baseline never saw?
3. In `baseline_mse`, which list should the mean come from, and what would it mean if you used the other one?
4. What should happen when there is nothing to average, and where is the earliest point to notice that?

## Explain-back

- Why is the mean the right constant for MSE, and what constant would you use if the metric were MAE?
- A model's validation MSE is 40 and the baseline's is 42. Is the model worth shipping? What would you want to know first?
- If you computed the baseline mean from the validation targets, why would its validation MSE be misleadingly low?
- Name a product situation where a constant prediction is actually good enough and a model is not worth building.
