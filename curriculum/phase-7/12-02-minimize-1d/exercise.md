# Minimize a 1-D function

Topic: 12. Optimization basics
Difficulty: 2 of 3

## Problem

Write `minimize_1d(f: Callable[[float], float], x0: float, lr: float, tol: float = 1e-8, max_steps: int = 10_000, h: float = 1e-5) -> tuple[float, int]` in pure Python (no NumPy).

Run gradient descent on a scalar function using the central-difference derivative `(f(x+h) - f(x-h)) / 2h` as the gradient. Stop when `|gradient| < tol` **before** taking a step (so a point that is already a minimum takes 0 steps), or when `max_steps` steps have been taken. Return `(x, steps_taken)`.

Raise `ValueError` if `lr <= 0`, `tol <= 0` or `max_steps < 0`. Raise `RuntimeError` if `|x|` exceeds `1e10` or becomes non-finite (`inf` or `nan`), which is what divergence looks like. (Beyond `1e10` the nudge `h` is smaller than a float step of `x`, so the numeric gradient would silently read `0`.)

## Examples

```
minimize_1d(lambda x: (x - 3) ** 2, x0=0.0, lr=0.1)      → (3.0 within 1e-6, some tens of steps)
minimize_1d(lambda x: (x - 3) ** 2, x0=3.0, lr=0.1)      → (3.0, 0)          already there
minimize_1d(lambda x: (x - 3) ** 2, x0=0.0, lr=0.1, max_steps=5)   → (1.9..., 5)   ran out of steps
minimize_1d(lambda x: x**4 - 3*x**2 + x, x0=2.0, lr=0.02)  → the right basin, x ≈ 1.13
minimize_1d(lambda x: x**4 - 3*x**2 + x, x0=-2.0, lr=0.02) → the left basin, x ≈ -1.30
minimize_1d(lambda x: x**2, x0=1.0, lr=1.5)               → RuntimeError    lr > 2/L
```

## Constraints

- With `tol = 1e-8` on a quadratic the returned `x` is within `1e-6` of the minimizer.
- A tighter `tol` must never take fewer steps than a looser one from the same start.
- The `steps_taken` count is exact: 0 when the start is already flat, `max_steps` when the budget runs out.

## Hints

1. Where in the loop does the tolerance check go so that a flat starting point reports 0 steps? What if you check after the update instead?
2. The gradient is `(f(x+h) - f(x-h)) / 2h`. Which of the last Topic's functions is this, and how many `f` calls does each step cost?
3. Without a divergence check, `lr = 1.5` on `x²` doubles `|x|` every step. Once `x` is around `1e11`, what does `x + 1e-5` evaluate to in float64, and what does the loop conclude?
4. Two starting points on `x⁴ - 3x² + x` end in different places. What property of the function makes that possible, and what would guarantee the same answer from any start?

## Explain-back

- Why is a tolerance on the gradient a better stopping rule than a fixed step count? Name a situation where the gradient tolerance is never reached.
- `lr = 1.5` diverges on `x²` but converges on `0.1·x²`. What does the safe learning rate depend on, and why is that a problem when you do not know the curvature?
- Gradient descent stopped at `x ≈ 1.13` on `x⁴ - 3x² + x`, which is not the global minimum. Is that a bug? What is the name of this outcome?
- With `tol = 1e-8` and `h = 1e-5`, what limits how close to the true minimizer you can get? Which of the two would you change first?
