# Cross-entropy from logits

Topic: 9. Multiclass: softmax regression and categorical cross-entropy
Difficulty: 2 of 3

## Problem

Categorical cross-entropy for one example is `−log softmax(z)[target]`. Taking the softmax first and then the log fails when a probability rounds to 0: `log(0)` is `−inf`. Work in log space with log-sum-exp instead. Write two NumPy functions:

- `log_softmax(logits: np.ndarray) -> np.ndarray` — along the last axis (1-D vector or 2-D `(n, C)`), computed as `z − logsumexp(z)` with the stable `logsumexp(z) = m + log Σ exp(z − m)`, where `m` is the row maximum. Same shape as the input. Every entry is finite for finite input.
- `cross_entropy_from_logits(logits: np.ndarray, target_idx) -> float` —
  - 1-D `logits` of length `C` and an `int` `target_idx`: returns `−log_softmax(logits)[target_idx]`.
  - 2-D `logits` of shape `(n, C)` and a length-`n` integer array `target_idx`: returns the **mean** loss over the rows.
  - Returns a Python `float`. Raise `ValueError` if a target is outside `0..C−1`, the number of targets does not match the number of rows, or `logits` is not 1-D or 2-D.

Neither function may trigger a NumPy overflow, divide or invalid warning, even on `[1000, 0]`. `scipy` is not allowed; write the log-sum-exp yourself.

## Examples

```
cross_entropy_from_logits(np.array([0.0, 0.0]), 0)          → 0.6931471805599453   log 2
cross_entropy_from_logits(np.array([1.0, 2.0, 3.0]), 2)     → 0.4076059644443804
cross_entropy_from_logits(np.array([1000.0, 0.0]), 1)       → 1000.0               finite, not inf
cross_entropy_from_logits(np.array([1000.0, 0.0]), 0)       → 0.0
cross_entropy_from_logits(np.array([[0.0, 0.0], [1000.0, 0.0]]), np.array([0, 1]))   → 500.3465735902799
log_softmax(np.array([1000.0, 1001.0]))                      → [-1.31326169, -0.31326169]
```

## Constraints

- NumPy allowed, vectorized over rows.
- `n` up to 100 000, `C` up to 1000.
- On moderate logits, equal to `−log(softmax(z)[target])` within `1e-10`.

## Hints

1. Write `log softmax(z)ᵢ` as `zᵢ` minus something. What is the something?
2. `log Σ exp(zⱼ)` overflows for `z = [1000, 0]`. Factor `e^m` out of the sum. What is left inside, and why can it no longer overflow?
3. After the shift, the sum inside the log is at least 1. Why does that guarantee the log is finite?
4. For a batch, how do you pick out `log_softmax[i, target_idx[i]]` for every row at once without a loop?

## Explain-back

- Why is `−log(softmax(z)[t])` unsafe for `z = [1000, 0]`, `t = 1`, and what does the log-sum-exp version return instead?
- Show that the cross-entropy loss depends only on the target's logit and the log-sum-exp of the row. What does the model gain by raising the target logit, and what does it lose by raising any other?
- PyTorch's `nn.CrossEntropyLoss` expects logits. What happens to training if you pass it probabilities from a softmax layer?
- How is this loss the negative log-likelihood of a categorical distribution, the same idea as BCE for two classes?
