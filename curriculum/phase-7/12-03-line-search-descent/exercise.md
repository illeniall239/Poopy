# Line-search descent

Topic: 12. Optimization basics
Difficulty: 3 of 3

## Problem

A fixed learning rate has to be tuned to the steepest direction of the loss; on a badly scaled problem it either diverges or crawls. Backtracking line search picks the step each iteration. Write, in pure Python (no NumPy; `math` allowed):

- `backtracking_step(f, x, fx, g, alpha0=1.0, beta=0.5, c=1e-4, max_halvings=60) -> float` — starting from `alpha = alpha0`, shrink `alpha *= beta` until the Armijo condition holds: `f(x - alpha·g) <= fx - c · alpha · ‖g‖²` (`fx` is `f(x)`, `g` the gradient at `x`). Return the accepted `alpha` (or the last tried one after `max_halvings`). Raise `ValueError` if `alpha0 <= 0`, `beta` is not in `(0, 1)` or `c` is not in `(0, 1)`.
- `line_search_descent(f, grad_f, x0, tol=1e-6, max_steps=1000) -> tuple[list[float], int]` — gradient descent where every step uses `backtracking_step`. Stop when `‖grad‖₂ < tol` before stepping, or after `max_steps`. Return `(x, steps_taken)`. Do not mutate `x0`.

## Examples

```
f = lambda v: 0.5 * (v[0]**2 + 20 * v[1]**2)       curvature 1 along x, 20 along y
g = lambda v: [v[0], 20 * v[1]]

backtracking_step(f, [10.0, 1.0], f([10.0, 1.0]), g([10.0, 1.0]))   → 0.0625   (1 halved four times)
backtracking_step(f, [10.0, 0.0], f([10.0, 0.0]), [10.0, 0.0])      → 1.0      one step to the minimum along x

line_search_descent(f, g, [10.0, 1.0])              → (≈ [0, 0], 125 steps)
fixed lr = 0.15 from the same start                 → y blows up (0.15 > 2/20)
fixed lr = 0.001 for 200 steps                      → x is still 8.2
```

## Constraints

- Up to 100 dimensions and 20 000 steps.
- The test checks that the Armijo condition holds for every returned `alpha`, that the loss never increases along the trajectory, and that the example converges to `‖x‖ < 1e-5` within 200 steps.
- Each call to `backtracking_step` evaluates `f` at most `max_halvings` times.

## Hints

1. The Armijo condition asks for "enough" decrease: at least a fraction `c` of what the linear approximation `f(x) - alpha·‖g‖²` promises. Why would accepting any decrease at all be too weak?
2. Start big and shrink: why `alpha0 = 1` and halving, rather than starting small and growing?
3. Along the `x` axis (curvature 1) a full step of `alpha = 1` lands on the minimum. Along `y` (curvature 20) it overshoots. What does backtracking do differently in the two cases, and what is the accepted `alpha` from `[10, 1]`?
4. When can the loop hit `max_halvings`? What must be true of `g` for the condition to be impossible to satisfy?

## Explain-back

- Why does one fixed learning rate struggle when curvature differs 20× between directions? What does feature scaling do to that ratio?
- Backtracking costs extra `f` evaluations per step. When is that a good trade, and why do deep-learning optimizers mostly avoid line search?
- The Armijo condition guarantees the loss decreases each step. Does that guarantee reaching the global minimum? Reaching a stationary point?
- On a saddle point the gradient is zero and your loop stops. Why are saddles, not local minima, the typical problem in high dimensions?
