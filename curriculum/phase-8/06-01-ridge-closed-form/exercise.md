# Ridge regression, closed form

Topic: 6. Overfitting, bias–variance and regularization
Difficulty: 1 of 3

## Problem

Write `ridge_closed_form(X: np.ndarray, y: np.ndarray, lam: float) -> tuple[np.ndarray, float]` with NumPy. It fits `ŷ = X w + b` by minimizing

```
Σᵢ (yᵢ − xᵢ·w − b)² + lam · ‖w‖²
```

and returns `(w, b)`: `w` a float array of shape `(d,)`, `b` a Python `float`.

The bias `b` is **not** penalized. The standard way to get that: center the columns of `X` and `y` on their training means, solve `(XcᵀXc + lam·I) w = Xcᵀ yc` for `w`, then recover `b = mean(y) − mean(X, axis=0) · w`. Adding a column of ones to `X` and putting it inside the penalty is the classic bug.

- `X` has shape `(n, d)`, `y` shape `(n,)`.
- `lam = 0` is ordinary least squares with an intercept (the tests use full-rank `X` there).
- As `lam` grows, `‖w‖` shrinks toward 0 and `b` tends to `mean(y)`, never to 0.
- Raise `ValueError` if `lam < 0`, if `X` is not 2-D, or if `len(y) != len(X)`.

## Examples

```
X = [[1.0], [2.0], [3.0]], y = [2.0, 4.0, 6.0]
ridge_closed_form(X, y, 0.0)   → (w=[2.0], b=0.0)
ridge_closed_form(X, y, 2.0)   → (w=[1.0], b=2.0)        (Xcᵀ Xc = 2, Xcᵀ yc = 4, so w = 4 / (2 + 2))
ridge_closed_form(X, y, 1e9)   → (w≈[0.0], b≈4.0)        b goes to mean(y)
ridge_closed_form(X, y, -1.0)  → ValueError
```

## Constraints

- NumPy allowed. Use `np.linalg.solve`, not an explicit matrix inverse.
- `n` up to 2000, `d` up to 50.
- Results within `1e-6` of the tests' reference values.

## Hints

1. Write the loss with `b` in it and set its derivative with respect to `b` to zero. What does `b` have to be, given `w`?
2. If you substitute that `b` back in, what happens to `X` and `y`? What problem is left for `w` alone?
3. Which matrix gets `lam` added to its diagonal, and how big is its identity: `d` or `d + 1`?
4. If you put a column of ones in `X` and let the penalty touch its weight, what does a huge `lam` do to predictions on data whose `y` sits around 100?

## Explain-back

- Why is the bias left out of the penalty? What would a penalized bias do to a model of house prices in dollars?
- L2 shrinks weights. Why does it almost never make one exactly zero?
- `lam` is a hyperparameter. Which data split do you choose it on, and why never the test set?
- Your model has high training error and high validation error. Should you raise `lam`? What would you do instead?
