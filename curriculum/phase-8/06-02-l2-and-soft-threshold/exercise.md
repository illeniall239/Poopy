# L2 step and soft-thresholding

Topic: 6. Overfitting, bias–variance and regularization
Difficulty: 2 of 3

## Problem

Write two NumPy functions that add a penalty to a gradient-descent update of a weight vector `w` (the bias is kept out of both: callers pass only the weights).

- `gd_step_with_l2(w: np.ndarray, grad: np.ndarray, lr: float, lam: float) -> np.ndarray` — one gradient step on `loss + (lam / 2) · ‖w‖²`, where `grad` is the gradient of `loss` alone. The penalty's gradient is `lam · w`, so the step is `w − lr · (grad + lam · w)`.
- `soft_threshold(w: np.ndarray, t: float) -> np.ndarray` — the L1 proximal step: every entry moves toward 0 by `t`, and any entry with `|wᵢ| ≤ t` becomes exactly `0.0`. That is `sign(wᵢ) · max(|wᵢ| − t, 0)`.

With these, one step of L1-regularized gradient descent (proximal gradient, "ISTA") on `loss + lam · ‖w‖₁` is `soft_threshold(w − lr · grad, lr · lam)`. The tests run that loop on a lasso problem and check it reaches scikit-learn's `Lasso` solution with exact zeros, while L2 never produces a zero.

Both functions return a **new** float array of the same shape and never modify their inputs. Raise `ValueError` if `lam < 0`, `lr <= 0`, `t < 0`, or `w` and `grad` differ in shape.

## Examples

```
gd_step_with_l2([1.0, -2.0], [0.0, 0.0], lr=0.1, lam=1.0)   → [0.9, -1.8]      pure shrink by (1 − lr·lam)
gd_step_with_l2([1.0], [2.0], lr=0.1, lam=0.0)              → [0.8]            plain gradient step
soft_threshold([3.0, -0.5, 0.2, -4.0], 1.0)                 → [2.0, 0.0, 0.0, -3.0]
soft_threshold([1.0, -1.0], 1.0)                            → [0.0, 0.0]        |w| == t becomes exactly 0
soft_threshold([1.0], -0.1)                                 → ValueError
```

## Constraints

- NumPy allowed, fully vectorized: no Python loop over entries.
- Arrays have up to 10 000 entries.
- Results within `1e-12` of the examples; the lasso loop's result within `1e-4` of scikit-learn.

## Hints

1. The L2 penalty's gradient is `lam · w`. Factor the step as `(something) · w − lr · grad`. What is the "something", and can it ever send a nonzero weight to exactly zero?
2. For the L1 step, think of one weight at a time. If `wᵢ = 3` and `t = 1`, where does it land? If `wᵢ = 0.4`?
3. Which NumPy functions give you the sign and the part of `|wᵢ| − t` that is above zero, without an `if` per entry?
4. How can you be sure you return a new array and leave the caller's `w` untouched?

## Explain-back

- Repeated L2 steps with a zero loss gradient multiply `w` by `(1 − lr·lam)` each time. Why does that never reach exactly 0, and why does soft-thresholding reach it in finitely many steps?
- Sketch the L1 and L2 penalty curves near `w = 0`. What about the L1 corner produces exact zeros?
- Why is the bias not passed to either function?
- Elastic net uses both penalties. What does each contribute when two features are strongly correlated?
