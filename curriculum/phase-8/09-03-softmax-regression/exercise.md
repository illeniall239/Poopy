# Softmax regression

Topic: 9. Multiclass: softmax regression and categorical cross-entropy
Difficulty: 3 of 3

## Problem

Train a multiclass linear classifier from scratch with NumPy. `X` has shape `(n, d)`, `y` holds `n` integer labels in `0..C−1`. The model has a weight matrix `W` of shape `(d, C)` and a bias vector `b` of shape `(C,)`; the logits are `Z = X W + b`, one row of `C` logits per example.

- `softmax_loss_and_grad(X: np.ndarray, y: np.ndarray, W: np.ndarray, b: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]` — returns `(loss, dW, db)`:
  - `loss`: the mean categorical cross-entropy over the rows, computed stably from the logits (log-sum-exp), as a Python `float`;
  - with `P = softmax(Z)` row-wise and `Y` the one-hot matrix of `y`, the gradient with respect to the logits is `(P − Y) / n`, so `dW = Xᵀ (P − Y) / n` (shape `(d, C)`) and `db` is the column sums of `(P − Y) / n` (shape `(C,)`).
- `train_softmax_regression(X: np.ndarray, y: np.ndarray, n_classes: int, lr: float, epochs: int) -> tuple[np.ndarray, np.ndarray, list[float]]` — full-batch gradient descent from `W = zeros((d, C))`, `b = zeros(C)`. Each epoch: compute `(loss, dW, db)` at the current parameters, append `loss` to `losses`, then `W -= lr · dW` and `b -= lr · db`. Return `(W, b, losses)`; `losses[0]` is therefore `log C`.
- `predict(X: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray` — the argmax of the logits in each row, as integer class indices.

No function may trigger a NumPy overflow, divide or invalid warning, even when the features are in the thousands. Raise `ValueError` from `train_softmax_regression` if `lr <= 0`, `epochs < 1`, `n_classes < 2`, `X` is not 2-D, `len(y) != len(X)`, or a label is outside `0..n_classes−1`.

## Examples

```
X = [[1.0, 0.0], [0.0, 1.0]], y = [0, 1], W = zeros((2, 2)), b = zeros(2)
softmax_loss_and_grad(X, y, W, b)
  → loss 0.6931471805599453,
    dW = [[-0.25, 0.25], [0.25, -0.25]],   P − Y = [[-0.5, 0.5], [0.5, -0.5]], divided by n = 2
    db = [0.0, 0.0]
W, b, losses = train_softmax_regression(three_blobs_X, three_blobs_y, 3, lr=0.1, epochs=300)
losses[0]                            → 1.0986122886681098   log 3
mean(predict(X, W, b) == y)          → above 0.9
```

## Constraints

- NumPy allowed, vectorized: no Python loop over rows or classes.
- `n` up to 5000, `d` up to 50, `C` up to 20, `epochs` up to 2000.
- `dW` and `db` must match central finite differences of `loss` within `1e-6`.

## Hints

1. Build the one-hot matrix `Y` without a loop. What does indexing `Y[np.arange(n), y]` select?
2. The loss for one row is `logsumexp(z) − z[target]`. Differentiate each piece with respect to `z`. What do you get, and why is there no softmax Jacobian left to multiply?
3. The gradient with respect to the logits has shape `(n, C)`. Which product with `X` gives a `(d, C)` gradient, and what does summing over rows give for `b`?
4. At epoch 0 every logit is 0. What is `P`, and what should the first recorded loss be?

## Explain-back

- Derive why the cross-entropy gradient with respect to the logits is `p − onehot`. Why do you never need to form the full softmax Jacobian?
- Why must the loss use log-sum-exp even though `predict` only needs an argmax?
- How does one-vs-rest logistic regression differ from softmax regression, and when might you prefer each?
- The decision boundary between two classes is where their logits are equal. Why is that boundary linear in the features?
