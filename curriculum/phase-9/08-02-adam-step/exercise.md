# Adam step

Topic: 8. Optimizers and learning-rate schedules
Difficulty: 2 of 3

## Problem

Write one step of Adam from its update equations, in plain Python (no numpy, and no `torch.optim`; do not use torch at all). For each parameter `p` with gradient `g`, at step number `t` (1 on the first step):

```
m ← b1 · m + (1 − b1) · g
v ← b2 · v + (1 − b2) · g²
m̂ = m / (1 − b1^t)
v̂ = v / (1 − b2^t)
p ← p − lr · m̂ / (√v̂ + eps)
```

`adam_step(params, grads, state, lr, b1, b2, eps, t)`:

- `params` is a list of floats; update it **in place** and return it (the same list object).
- `grads` is a list of floats, one per parameter.
- `state` is a dict. On the first step it is empty `{}`: create `state["m"]` and `state["v"]` as lists of `0.0`, one per parameter. After every step they hold the new `m` and `v` (the raw moving averages, not the bias-corrected ones).
- `t` is the 1-based step number; the caller increases it by 1 every call.

The result must match `torch.optim.Adam(lr=lr, betas=(b1, b2), eps=eps)` over a sequence of steps within `1e-9`.

Raise `ValueError` (without changing anything) if `grads` and `params` differ in length, if `t < 1`, if `b1` or `b2` is not in `[0, 1)`, if `lr <= 0` or `eps <= 0`, or if `state` is not empty and its `m` or `v` has the wrong length.

## Examples

```
params, state = [1.0, -1.0], {}
adam_step(params, [0.2, -3.0], state, 0.1, 0.9, 0.999, 1e-8, 1)
    → [0.900000005, -0.9000000003333]     each moves by almost exactly lr: m̂/√v̂ = ±1 on step 1
state["m"] → [0.02, -0.3]
state["v"] → [4e-05, 0.009]

params = [5.0]; adam_step(params, [0.0], {}, 0.1, 0.9, 0.999, 1e-8, 1) → [5.0]
```

Without the bias correction the first step would move each parameter by about `0.1 · 0.1 / √0.001 ≈ 0.32` instead of `0.1`.

## Constraints

- Plain Python lists of floats, at most 100 000 entries.
- Up to 10 000 steps.

## Hints

1. `m` and `v` both start at 0. After one step with `b1 = 0.9`, how big is `m` compared with the gradient? What about `v` compared with `g²` when `b2 = 0.999`?
2. What do you divide `m` by so that, on step 1, it equals the gradient exactly? Does the same correction work on step `t`?
3. On the first step, what does `m̂ / √v̂` equal for any nonzero `g`? What does that tell you about the size of Adam's first step?
4. Where does `eps` go: inside the square root or outside it? Which placement does PyTorch use?

## Explain-back

- What goes wrong in the first few steps if you skip the bias correction? Would the steps be too big or too small, and by roughly how much with the default betas?
- Why is Adam's step size roughly `lr` regardless of how big the gradient is, and when is that a weakness?
- An L2 penalty added to the loss goes through `m` and `v`; AdamW's weight decay does not. Why does that make them different for Adam when they are the same for plain SGD?
- Adam usually converges faster. Why might a CNN trained with SGD plus momentum still generalize better?
