# Regression metrics

Topic: 2. Linear regression and MSE, closed form
Difficulty: 1 of 3

## Problem

Write four pure-Python functions (no numpy) that score regression predictions. Each takes `y_true: list[float]` and `y_pred: list[float]` and raises `ValueError` if the lists are empty or their lengths differ.

- `mse(y_true, y_pred) -> float` — mean of the squared residuals `(yᵢ − ŷᵢ)²`.
- `mae(y_true, y_pred) -> float` — mean of the absolute residuals `|yᵢ − ŷᵢ|`.
- `rmse(y_true, y_pred) -> float` — the square root of the MSE, in the target's own units.
- `r2(y_true, y_pred) -> float` — the coefficient of determination `1 − SS_res / SS_tot`, where `SS_res = Σ (yᵢ − ŷᵢ)²` and `SS_tot = Σ (yᵢ − ȳ)²` with `ȳ` the mean of `y_true`. It is `1.0` for a perfect prediction, `0.0` for predicting `ȳ` everywhere, and negative for predictions worse than that. Raise `ValueError` if every `y_true` is the same value (`SS_tot = 0`, so R² is undefined).

## Examples

```
mse([1, 2, 3], [1, 2, 5])          → 1.3333...   (0 + 0 + 4) / 3
mae([1, 2, 3], [1, 2, 5])          → 0.6666...
rmse([1, 2, 3], [1, 2, 5])         → 1.1547...
r2([1, 2, 3], [1, 2, 3])           → 1.0
r2([1, 2, 3], [2, 2, 2])           → 0.0          the mean, everywhere
r2([1, 2, 3], [3, 2, 1])           → -3.0         worse than the mean
r2([5, 5, 5], [5, 5, 5])           → ValueError   SS_tot is 0
```

## Constraints

- Pure Python: `math` is allowed, numpy is not.
- Up to 100 000 values; each function is O(n).
- Results within `1e-9` of `sklearn.metrics`.

## Hints

1. Which of these metrics are in the target's units and which are in squared units? What does that mean when you report one to someone who does not know ML?
2. One residual of 100 and ninety-nine residuals of 1: how much of the MSE comes from the one big residual, and how much of the MAE?
3. What does R² compare your model against? What is `SS_res` when the prediction is `ȳ` for every row?
4. Is there a lower bound on R²? What prediction would make `SS_res` larger than `SS_tot`, and what happens to the ratio when `SS_tot` is zero?

## Explain-back

- A model has a negative R² on the validation set. What does that say, and what trivial model beats it?
- House prices contain a few mansions worth 50× the median. Which metric would you train and report with, and why?
- R² is 0.95 on a fit of city crime against the number of police officers. What can you conclude, and what can't you?
- Why is RMSE usually preferred over MSE for reporting, even though the model is often trained on MSE?
