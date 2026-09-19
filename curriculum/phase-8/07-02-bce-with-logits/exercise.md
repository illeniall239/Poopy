# BCE with logits

Topic: 7. Logistic regression and binary cross-entropy
Difficulty: 2 of 3

## Problem

Binary cross-entropy is the negative log-likelihood of a Bernoulli label: for probability `p = σ(z)` and label `y`, the loss is `−[y·log p + (1 − y)·log(1 − p)]`. Computing `p` first and then `log p` fails when `p` rounds to exactly 0 or 1. Work from the logit `z` instead. Write two NumPy functions:

- `bce_with_logits(z: np.ndarray, y: np.ndarray) -> float` — the **mean** BCE over all elements, computed with the stable form

  ```
  max(z, 0) − z·y + log(1 + e^(−|z|))
  ```

  (use `np.log1p`). Return a Python `float`.
- `bce_with_logits_grad(z: np.ndarray, y: np.ndarray) -> np.ndarray` — the gradient of that mean loss with respect to each `zᵢ`: `(σ(zᵢ) − yᵢ) / n`, where `n` is the number of elements. Same shape as `z`. Use a sigmoid that cannot overflow.

`z` and `y` have the same shape (any shape); `y` holds labels in `[0, 1]`. Neither function may trigger a NumPy overflow, divide or invalid warning, even for `|z| = 1000`. Raise `ValueError` if the shapes differ or the arrays are empty.

## Examples

```
bce_with_logits([0.0], [1.0])              → 0.6931471805599453   log 2
bce_with_logits([1000.0], [0.0])           → 1000.0               confidently wrong: huge, but finite
bce_with_logits([1000.0], [1.0])           → 0.0
bce_with_logits([-1000.0, 2.0], [1.0, 1.0]) → 500.0634640...      (1000 + 0.126928) / 2
bce_with_logits_grad([0.0, 0.0], [1.0, 0.0]) → [-0.25, 0.25]
```

## Constraints

- NumPy allowed, vectorized.
- Arrays up to 1 000 000 elements.
- On moderate logits (`|z| ≤ 20`) the loss equals the naive formula within `1e-10`; the gradient matches central finite differences of your own loss within `1e-6`.

## Hints

1. Write `log σ(z)` and `log(1 − σ(z))` in terms of `z` and `log(1 + e^(−z))`. What does the whole loss simplify to?
2. The simplified loss contains `log(1 + e^(−z))`. For which `z` does that overflow, and how does splitting on the sign of `z` (or using `|z|`) fix it?
3. Why `np.log1p(x)` instead of `np.log(1 + x)` when `x` is tiny?
4. Differentiate `max(z, 0) − z·y + log(1 + e^(−|z|))` on each side of 0. Do both sides give the same simple expression?

## Explain-back

- A model outputs `p = 1.0` exactly for a negative example. What does naive BCE return, and what does the logit version return?
- Why is BCE, not MSE, the loss for logistic regression? Say what goes wrong with MSE after the sigmoid.
- Why does the gradient come out as the plain `p − y` with no `σ'(z)` factor?
- PyTorch has both `BCELoss` and `BCEWithLogitsLoss`. Which should a model with a final linear layer use, and why?
