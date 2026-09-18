# MSE gradient

Topic: 11. Partial derivatives, gradients and Jacobians
Difficulty: 2 of 3

## Problem

For a line `ŷ = w·x + b` and data `xs`, `ys` of equal length `n`, the mean squared error is `L(w, b) = (1/n) Σ (ŷᵢ - yᵢ)²`. Write, in pure Python (no NumPy):

- `mse(w: float, b: float, xs: list[float], ys: list[float]) -> float` — the loss.
- `mse_gradient(w: float, b: float, xs: list[float], ys: list[float]) -> tuple[float, float]` — the analytic gradient `(∂L/∂w, ∂L/∂b)`:
  `∂L/∂w = (2/n) Σ (ŷᵢ - yᵢ) xᵢ` and `∂L/∂b = (2/n) Σ (ŷᵢ - yᵢ)`.

Both raise `ValueError` if the lengths differ or `n == 0`.

## Examples

```
xs, ys = [1, 2, 3], [2, 4, 6]          the line y = 2x
mse(2.0, 0.0, xs, ys)                  → 0.0
mse_gradient(2.0, 0.0, xs, ys)         → (0.0, 0.0)        at the minimum
mse(0.0, 0.0, xs, ys)                  → 18.666...          (4 + 16 + 36) / 3
mse_gradient(0.0, 0.0, xs, ys)         → (-18.666..., -8.0)
mse_gradient(1.0, 1.0, xs, ys)         → (-5.333..., -2.0)  residuals 0, -1, -2
```

## Constraints

- Up to 100 000 points; one pass over the data.
- The gradient must match a central-difference numeric gradient with `h = 1e-5` within `1e-6` on several random datasets.
- A step `w -= 0.01 · ∂L/∂w`, `b -= 0.01 · ∂L/∂b` must lower the loss on the example data.

## Hints

1. Write `L` as `(1/n) Σ rᵢ²` with `rᵢ = w xᵢ + b - yᵢ`. What is `∂rᵢ/∂w` and `∂rᵢ/∂b`?
2. Apply the chain rule to `rᵢ²`: what is the outer derivative, and what multiplies it for `w` versus for `b`?
3. Where does the `2/n` come from? Check it with `xs = [1]`, `ys = [0]`, `w = 1`, `b = 0` by hand.
4. Both partials share the residuals. Can you compute them once and reuse them in one loop?

## Explain-back

- Why is `∂L/∂b` a sum of residuals while `∂L/∂w` weights each residual by `xᵢ`? What does that say about which points pull `w` hardest?
- The gradient at `(0, 0)` is `(-18.7, -8)`. In which direction should `w` and `b` move to reduce the loss, and why the sign flip?
- The gradient of MSE is a sum over data points. In an autograd engine, what does that sum correspond to when the same parameter is used by many examples?
- If `xs` were measured in millimetres instead of metres, what would happen to `∂L/∂w` compared with `∂L/∂b`, and why does that make a single learning rate awkward?
