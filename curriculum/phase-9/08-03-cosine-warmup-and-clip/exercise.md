# Cosine warmup and gradient clipping

Topic: 8. Optimizers and learning-rate schedules
Difficulty: 2 of 3

## Problem

Write two tools that most modern training loops use. Use plain Python and NumPy; do not use `torch.optim.lr_scheduler` or `torch.nn.utils.clip_grad_norm_` (the tests compare against the latter).

**`cosine_lr(step, total, base, warmup)`** returns the learning rate for integer `step`, with `0 ≤ step ≤ total`:

- Linear warmup: for `step < warmup`, the rate is `base · step / warmup` (so step 0 gives 0).
- Cosine decay: for `step ≥ warmup`, with `progress = (step − warmup) / (total − warmup)`, the rate is `base · 0.5 · (1 + cos(π · progress))`: it equals `base` at `step == warmup` and falls to `0` at `step == total`.

Return a Python `float`. Raise `ValueError` if `step < 0`, `step > total`, `base <= 0`, `warmup < 0` or `warmup >= total`.

**`clip_grad_norm(grads, max_norm)`** clips by the **global** norm:

- `grads` is a list of NumPy float arrays of any shapes (one per parameter).
- The global norm is `√(sum of the squares of every element of every array)`.
- If that norm is greater than `max_norm`, multiply **every** array, in place, by `max_norm / norm`, so the new global norm is exactly `max_norm` and every gradient keeps its direction. Otherwise leave them alone.
- Return the global norm measured **before** clipping, as a Python `float`.

An empty list has norm `0.0`. Raise `ValueError` if `max_norm <= 0`.

## Examples

```
cosine_lr(0,   100, 1.0, 10) → 0.0
cosine_lr(5,   100, 1.0, 10) → 0.5       halfway through warmup
cosine_lr(10,  100, 1.0, 10) → 1.0       peak
cosine_lr(55,  100, 1.0, 10) → 0.5       halfway through the decay
cosine_lr(100, 100, 1.0, 10) → 0.0
cosine_lr(0,   100, 0.3, 0)  → 0.3       no warmup

g = [np.array([3.0]), np.array([4.0])]
clip_grad_norm(g, 1.0) → 5.0             g is now [array([0.6]), array([0.8])]
g = [np.array([3.0, 4.0])]
clip_grad_norm(g, 10.0) → 5.0            unchanged
```

Clipping each element to `[−1, 1]` would have turned `[3, 4]` into `[1, 1]` and changed the direction; global-norm clipping gives `[0.6, 0.8]`.

## Constraints

- `total` at most 10 000 000.
- `grads` holds at most 1000 arrays and 10 000 000 elements in total.
- `clip_grad_norm` matches `torch.nn.utils.clip_grad_norm_` within `1e-6` relative (PyTorch adds `1e-6` to the norm before dividing).

## Hints

1. Where does the warmup line start and end? Write the rate at `step = 0` and at `step = warmup`.
2. What values does `0.5 · (1 + cos(π · x))` take at `x = 0`, `0.5` and `1`? How do you map the steps after warmup onto `x` in `[0, 1]`?
3. What is the difference between clipping each element and scaling every gradient by the same factor? Which one keeps the direction of the whole update?
4. How do you compute one norm across arrays of different shapes, and how do you rescale an array so the caller's array changes, not a copy?

## Explain-back

- Why warm up at all? What can go wrong in the first steps of training a large network (especially with Adam) at the full learning rate?
- Why does cosine decay tend to beat a constant rate at the end of training?
- Why clip by the global norm rather than per element or per parameter? What does per-element clipping do to the direction of the update?
- Why return the norm before clipping? What would you learn from logging it over a run?
