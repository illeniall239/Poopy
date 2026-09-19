# Permutation importance

Topic: 13. Interpretability for tabular models
Difficulty: 1 of 3

## Problem

Permutation importance asks a trained model one question per feature: how much worse do you get if this column is scrambled? Write it with NumPy:

```
permutation_importance(predict, X: np.ndarray, y: np.ndarray, metric, rng: np.random.Generator, repeats: int = 5) -> np.ndarray
```

- `predict` maps an `(n, d)` array to `n` predictions. It is an already-trained model: never retrain anything.
- `metric(y_true, y_pred) -> float` is higher-is-better (accuracy, R², negative MSE).
- First compute `baseline = metric(y, predict(X))`.
- For each feature `j = 0, 1, …, d−1` in order, and for each of the `repeats` repeats in turn: copy `X`, replace column `j` of the copy with `rng.permutation(X[:, j])`, and record `baseline − metric(y, predict(copy))`. Exactly one `rng.permutation` call per (feature, repeat), in that order, so a given seed gives the same answer as the test's replay.
- Return a float array of shape `(d,)` holding each feature's mean drop over its repeats.

Do not modify `X`. Raise `ValueError` if `repeats < 1`, `X` is not 2-D, or `len(X) != len(y)`.

A feature the model ignores has importance exactly `0.0`. A negative value means shuffling happened to help: the feature is useless, not harmful.

## Examples

```
X = np.array([[1.0, 5.0], [2.0, 5.0], [3.0, 7.0], [4.0, 7.0]])
y = X[:, 0] * 2
predict = lambda A: A[:, 0] * 2               # ignores column 1
neg_mse = lambda t, p: -np.mean((t - p) ** 2)
permutation_importance(predict, X, y, neg_mse, np.random.default_rng(0), repeats=3)
    → array([importance > 0, 0.0])
```

## Constraints

- NumPy allowed; no scikit-learn.
- `n` ≤ 2 000, `d` ≤ 10, `repeats` ≤ 20: `d · repeats` calls to `predict`, plus one.
- The result matches the test's replay within `1e-12`.

## Hints

1. Why shuffle a column instead of deleting it or setting it to zero? Which property of the column does shuffling keep, and which link does it break?
2. What do you need to compute once, before any shuffling, so every drop is measured against the same thing?
3. If you shuffle column `j` in place in `X`, what happens to the drop you then measure for column `j + 1`?
4. Why average several shuffles instead of using one? What makes one shuffle of a small dataset an unreliable measurement?

## Explain-back

- Why should permutation importance be computed on held-out data, not on the training set? What would an overfit model show on its training rows?
- Two columns are near copies of each other and the model uses both. What happens to each one's importance when you shuffle it alone, and what wrong conclusion could you draw?
- The model ranks "number of support tickets" as the top feature for churn. Does that mean more tickets cause churn? What can this number claim and what can it not?
- How is this different from a random forest's impurity-based importance, and which bias of impurity importance does it avoid?
