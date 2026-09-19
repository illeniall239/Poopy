# Gradient descent for a line

Topic: 3. Gradient descent for linear regression
Difficulty: 1 of 3

## Problem

Write `gd_linreg_1d(xs: list[float], ys: list[float], lr: float, epochs: int) -> tuple[float, float, list[float]]` in pure Python (no numpy) that fits `ŷ = w·x + b` by full-batch gradient descent on the mean squared error `L = (1/n) Σ (w·xᵢ + b − yᵢ)²`.

- Start from `w = 0.0`, `b = 0.0`.
- Each epoch computes both gradients from the current `w` and `b` over all `n` points,
  `∂L/∂w = (2/n) Σ (ŷᵢ − yᵢ)·xᵢ` and `∂L/∂b = (2/n) Σ (ŷᵢ − yᵢ)`,
  then updates both at once: `w -= lr · ∂L/∂w`, `b -= lr · ∂L/∂b`. The update for `b` must use the gradient computed before `w` changed.
- Return `(w, b, loss_history)` where `loss_history` has `epochs + 1` entries: the MSE at the start (with `w = b = 0`) and the MSE after each epoch's update.

Raise `ValueError` if the lists are empty or their lengths differ, if `lr <= 0`, or if `epochs < 0`. With `epochs = 0`, return `(0.0, 0.0, [initial MSE])`.

With a small enough learning rate the loss never increases and `(w, b)` converges to the closed-form least-squares line. With a learning rate that is too large the loss grows every epoch; the function must still return normally (for the modest epoch counts tested, the numbers stay finite).

## Examples

```
gd_linreg_1d([1, 2, 3], [2, 4, 6], 0.1, 0)      → (0.0, 0.0, [18.6667])
gd_linreg_1d([1, 2, 3], [2, 4, 6], 0.1, 1)      → (1.8667, 0.8, [18.6667, 0.2963])
gd_linreg_1d(xs, ys, 0.1, 3000)                 → (w, b) within 1e-6 of the closed form, for xs in [-1, 1]
```

## Constraints

- Pure Python: `math` is allowed, numpy is not.
- At most 1 000 points and 5 000 epochs; O(n) per epoch.
- `loss_history` is non-increasing (within `1e-12`) for the stable learning rates tested.

## Hints

1. The loss is a bowl in `(w, b)`. Which direction does the gradient point, and why do you step against it?
2. Differentiate `(w·x + b − y)²` with respect to `w` and to `b`. What is the only difference between the two expressions?
3. If you update `w` first and then compute the gradient for `b`, which `w` does that gradient see? Why is that a different algorithm?
4. With `xs` around 1 000 instead of around 1, how big is `∂L/∂w` compared with `∂L/∂b`, and what does that do to a learning rate that worked before?

## Explain-back

- Why does gradient descent reach the same line as the closed form, and why would you ever use it when the closed form exists?
- The loss goes `18, 40, 95, 230, …`. What went wrong, and what two things would you check first?
- What is the difference between a parameter and a hyperparameter here? Name each one in this function.
- Why is the loss curve of full-batch gradient descent smooth, while the one from stochastic gradient descent is noisy, and is that noise a bug?
