# Gradient boosting with stumps

Topic: 12. Ensembles: bagging, random forests and gradient boosting
Difficulty: 2 of 3

## Problem

Gradient boosting builds a model one small correction at a time: each new model is fitted to what the ensemble so far still gets wrong. Write it for 1-D regression with squared error, in pure Python:

- `gradient_boost_stumps(xs: list[float], ys: list[float], n_rounds: int, lr: float) -> dict`
- `predict_boosted(model: dict, x: float) -> float`

The algorithm:

1. Start from the constant `base = mean(ys)`, so every training prediction is `base`.
2. Each round, compute the residuals `rᵢ = yᵢ − predictionᵢ` and fit a **stump** to them: a threshold `t` with a `left_value` for `x <= t` and a `right_value` for `x > t`. Candidate thresholds are the midpoints between consecutive distinct sorted `xs`; each side's value is the mean residual on that side; pick the threshold with the smallest sum of squared errors on the residuals, ties (within `1e-12`) going to the smaller threshold.
3. Add the stump scaled by the learning rate: `predictionᵢ += lr · stump(xᵢ)`.

Return a dict with exactly these keys:

- `"base"`: the starting mean,
- `"lr"`: the learning rate,
- `"stumps"`: the list of `(threshold, left_value, right_value)` tuples, one per round, in order,
- `"losses"`: the training MSE before any stump and after each round, so `len(losses) == n_rounds + 1`.

`predict_boosted(model, x)` returns `base + lr · Σ stump(x)` over all stumps. `n_rounds = 0` gives the constant model.

Raise `ValueError` if `xs` is empty, `len(xs) != len(ys)`, `xs` has fewer than two distinct values, `n_rounds < 0`, or `lr` is not in `(0, 1]`.

## Examples

```
xs = [1.0, 2.0, 3.0, 4.0];  ys = [0.0, 0.0, 10.0, 10.0]
m = gradient_boost_stumps(xs, ys, n_rounds=1, lr=1.0)
m["base"]                → 5.0
m["stumps"]              → [(2.5, -5.0, 5.0)]
m["losses"]              → [25.0, 0.0]
predict_boosted(m, 1.0)  → 0.0
m = gradient_boost_stumps(xs, ys, n_rounds=1, lr=0.1)
predict_boosted(m, 1.0)  → 4.5        only 10% of the way from 5 to 0
predict_boosted(m, 99.0) → 5.5        same as at x = 4: no extrapolation
```

## Constraints

- Pure Python, no numpy.
- Tests use at most 60 points and 60 rounds; an O(n²) stump search per round is fast enough.
- Losses and predictions within `1e-8` of the exact values.

## Hints

1. After the first round, what exactly is the next stump trying to predict: `ys`, or something else? Write down the target for round 2 in terms of `ys` and the current predictions.
2. For a fixed threshold, what single number per side minimizes the squared error of the residuals on that side?
3. Why does adding `lr · stump` with `lr` in `(0, 1]` never make the training loss worse, as long as the stump itself reduced the squared error of the residuals?
4. What must you keep from each round so that `predict_boosted` can rebuild the prediction for an `x` it has never seen?

## Explain-back

- Bagging averages many independent-ish models to cut variance. Which error does boosting attack instead, and why do stumps (very biased models) work well as its building block?
- Your training loss drops every single round. Why is that not a reason to run 5 000 rounds, and how would you pick `n_rounds` honestly?
- What does a smaller `lr` do to the number of rounds you need and to overfitting?
- The residual `y − ŷ` is the negative gradient of `½(y − ŷ)²` with respect to `ŷ`. What would a boosting round fit instead if the loss were absolute error?
