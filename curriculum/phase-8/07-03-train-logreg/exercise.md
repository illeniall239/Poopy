# Train logistic regression

Topic: 7. Logistic regression and binary cross-entropy
Difficulty: 2 of 3

## Problem

Write a from-scratch logistic regression trainer with NumPy. `X` has shape `(n, d)`, `y` shape `(n,)` with labels `0` or `1`.

- `train_logreg(X: np.ndarray, y: np.ndarray, lr: float, epochs: int) -> tuple[np.ndarray, float, list[float]]` — full-batch gradient descent on the mean binary cross-entropy. Start from `w = zeros(d)`, `b = 0.0`. Each epoch:
  1. compute logits `z = X w + b`;
  2. record the mean BCE at the **current** parameters in `losses` (so `losses[0]` is `log 2`);
  3. update with the gradient: `w -= lr · Xᵀ(p − y) / n` and `b -= lr · mean(p − y)`, where `p = σ(z)`.

  Return `(w, b, losses)` with `w` of shape `(d,)`, `b` a Python `float`, and `losses` a list of `epochs` Python floats.
- `predict_proba(X: np.ndarray, w: np.ndarray, b: float) -> np.ndarray` — `σ(X w + b)` for every row.
- `predict(X: np.ndarray, w: np.ndarray, b: float, threshold: float = 0.5) -> np.ndarray` — integer labels: `1` where the probability is `>= threshold`, else `0`.

The loss and the sigmoid must be the stable versions: on unscaled data the logits reach the hundreds, and the tests fail on any NumPy overflow, divide or invalid warning. Raise `ValueError` if `lr <= 0`, `epochs < 1`, `X` is not 2-D, or `len(y) != len(X)`.

## Examples

```
X = [[0.0], [1.0], [2.0], [3.0]], y = [0, 0, 1, 1]
train_logreg(X, y, lr=0.5, epochs=1)      → (w=[0.25], b=0.0, losses=[0.6931471805599453])
                                            p = 0.5 everywhere, so the w-gradient is Xᵀ(0.5 − y) / 4 = −0.5
w, b, _ = train_logreg(X, y, lr=0.5, epochs=2000)
predict(X, w, b)                          → [0, 0, 1, 1]
predict(X, w, b, threshold=0.999)         → fewer 1s: a stricter threshold trades recall for precision
```

## Constraints

- NumPy allowed, vectorized over rows: no Python loop over samples.
- `n` up to 5000, `d` up to 20, `epochs` up to 5000.
- With a small enough step size (the tests use one well below `4 / λ_max(XᵀX / n)`), the recorded losses never increase.

## Hints

1. The gradient of mean BCE with respect to the logits is `(p − y) / n`. How does the chain rule carry that to `w` and to `b`?
2. In what order must you record the loss and apply the update so that `losses[0]` is the loss of the all-zeros model?
3. On a feature measured in thousands, what logits does the model produce after a few steps, and what would a naive `1 / (1 + np.exp(-z))` do with them?
4. Once the model is trained, what changes when you move the threshold from 0.5 to 0.9, and what stays the same?

## Explain-back

- The decision boundary is where `p = 0.5`. Write its equation in terms of `w` and `b`. Why is it a straight line (a hyperplane) even though the sigmoid curves?
- On perfectly separable data, what happens to `‖w‖` as you keep training, and why? What would stop it?
- Why is 0.5 not a law? Give a case where you would use 0.2.
- Why train on BCE instead of MSE on the probabilities, and how would you add class weights if only 2% of the labels were 1?
