# SGD with momentum

Topic: 8. Optimizers and learning-rate schedules
Difficulty: 1 of 3

## Problem

Write one step of SGD with momentum, in plain Python (no numpy, no torch), using the same update as `torch.optim.SGD(momentum=beta)`:

```
v ← beta · v + g
p ← p − lr · v
```

`sgd_momentum_step(params, grads, state, lr, beta)`:

- `params` is a list of floats; update it **in place**.
- `grads` is a list of floats, one gradient per parameter.
- `state` is the list of velocities from the previous step, one per parameter. On the very first step it is an empty list: treat every velocity as `0.0` and fill `state` in place with the new velocities. On later steps overwrite its values in place.
- `lr > 0` is the learning rate; `beta` in `[0, 1)` is the momentum coefficient. `beta = 0` is plain SGD.

Return `state`, the same list object, now holding the new velocities.

Raise `ValueError` (without changing anything) if `grads` and `params` differ in length, if `state` is neither empty nor the same length as `params`, if `lr <= 0`, or if `beta` is not in `[0, 1)`.

## Examples

```
params, state = [1.0, -2.0], []
sgd_momentum_step(params, [0.5, -1.0], state, 0.1, 0.9)  → [0.5, -1.0]
params                                                   → [0.95, -1.9]
sgd_momentum_step(params, [0.5, -1.0], state, 0.1, 0.9)  → [0.95, -1.9]    0.9·0.5 + 0.5
params                                                   → [0.855, -1.71]

sgd_momentum_step([1.0], [2.0], [], 0.1, 0.0)            → [2.0]           plain SGD: p becomes 0.8
```

## Constraints

- Plain Python lists of floats, at most 100 000 entries.
- Values match `torch.optim.SGD(lr=lr, momentum=beta)` within `1e-9` over many steps.

## Hints

1. What does the velocity remember that the current gradient alone does not?
2. On the very first step there is no previous velocity. What value makes the formula give the same thing PyTorch does?
3. How do you change the values inside a list the caller passed in, instead of making a new list that the caller never sees?
4. If the gradient stays the same forever, what value does `v` settle to? What does that say about the effective step size with `beta = 0.9`?

## Explain-back

- With a constant gradient, the velocity approaches `g / (1 − beta)`. What does that mean for the effective learning rate at `beta = 0.9`, and why do people sometimes lower `lr` when they add momentum?
- Why does momentum help on a long, narrow valley where plain SGD zig-zags?
- Nesterov momentum evaluates the gradient at a "looked-ahead" point. In words, what does that change?
- Adam is often the default. Why might plain SGD with momentum still be the better choice for training a CNN?
