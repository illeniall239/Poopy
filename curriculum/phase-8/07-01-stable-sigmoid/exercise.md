# Stable sigmoid

Topic: 7. Logistic regression and binary cross-entropy
Difficulty: 1 of 3

## Problem

The sigmoid `σ(z) = 1 / (1 + e^(−z))` turns a logit into a probability. Written naively, `math.exp(-z)` raises `OverflowError` once `−z` is above about 709. Write two versions that never overflow:

- `stable_sigmoid(z: float) -> float` — pure Python with `math`. Returns a Python `float`.
- `stable_sigmoid_np(z: np.ndarray) -> np.ndarray` — NumPy, vectorized, any shape. Returns a float array of the same shape and must not trigger any NumPy overflow, divide or invalid warning (the tests turn those into errors with `np.errstate`).

The trick uses the sign of `z` so that `exp` only ever sees a non-positive number:

- for `z ≥ 0`: `1 / (1 + e^(−z))`
- for `z < 0`: `e^z / (1 + e^z)` (the same value, rearranged)

Requirements:

- `σ(1000) == 1.0` and `σ(−1000) == 0.0` exactly, with no exception or warning.
- On moderate inputs, within `1e-12` relative error of the textbook formula.
- Small tail probabilities keep their precision: `σ(−30)` must be within relative `1e-12` of `e^(−30) / (1 + e^(−30))`. Computing it as `1 − σ(30)` loses almost every digit.
- Catching the `OverflowError` with `try/except` is not the fix: the point is to never compute the huge number.

## Examples

```
stable_sigmoid(0.0)       → 0.5
stable_sigmoid(2.0)       → 0.8807970779778823
stable_sigmoid(-2.0)      → 0.11920292202211755
stable_sigmoid(1000.0)    → 1.0
stable_sigmoid(-1000.0)   → 0.0
stable_sigmoid_np(np.array([-1000.0, 0.0, 1000.0]))   → array([0. , 0.5, 1. ])
```

## Constraints

- `stable_sigmoid`: pure Python, `math` only.
- `stable_sigmoid_np`: NumPy, no Python loop over elements. Note that `np.where` evaluates **both** branches on every element, so each branch must itself be safe for all inputs.
- Arrays up to 1 000 000 elements.

## Hints

1. For which sign of `z` does `e^(−z)` blow up? For that sign, what happens to `e^z` instead?
2. Multiply the top and bottom of `1 / (1 + e^(−z))` by `e^z`. What do you get, and when is it safe to compute?
3. Both forms only ever need `e^(−|z|)`. Can you compute that once and build both branches from it?
4. Why does `1 − σ(30)` give a poor answer for `σ(−30)`? How many significant digits does `1 − 0.99999999999990641` keep?

## Explain-back

- Why is `try/except OverflowError: return 0.0` the wrong fix, even though it gives the right answer at `z = 1000`?
- What does the output of a sigmoid mean for logistic regression, and why is the model still called a *linear* classifier when the sigmoid curves?
- Why does computing `σ(−30)` as `1 − σ(30)` lose precision? Where else in ML does subtracting two nearly equal numbers bite?
- Logistic regression is a classifier. Why is it called "regression"?
