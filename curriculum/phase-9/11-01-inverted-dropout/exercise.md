# Inverted dropout

Topic: 11. Regularization in deep nets
Difficulty: 1 of 3

## Problem

Write `dropout(x, p, rng, training)` in plain Python (no numpy, no torch). It applies **inverted dropout** to a list of activations `x`:

- `p` is the probability of dropping a unit, with `0 <= p < 1`. Raise `ValueError` otherwise.
- `rng` is a `random.Random`. When `training` is `True`, draw exactly one `rng.random()` per element, in order. The element is **dropped** (becomes `0.0`) when its draw is `< p`; otherwise it is **kept and scaled** by `1 / (1 - p)`.
- When `training` is `False`, return the activations unchanged (as a new list of floats) and do not touch `rng` at all.

Always return a new list of floats, the same length as `x`; never modify `x`. With `p = 0` training mode is the identity (it still draws one number per element). Because of the scaling, the mean output over many random seeds equals the input: tests check this within a tolerance of `0.1` over 2000 seeds.

## Examples

```
dropout([1.0, 2.0, 3.0], 0.5, random.Random(0), training=False)  → [1.0, 2.0, 3.0]
dropout([1.0, 2.0, 3.0], 0.0, random.Random(0), training=True)   → [1.0, 2.0, 3.0]
dropout([2.0, 2.0, 2.0, 2.0], 0.5, rng, True)                    → each entry is 0.0 or 4.0
dropout([], 0.3, random.Random(0), True)                         → []
dropout([1.0], 1.0, random.Random(0), True)                      → ValueError
```

## Constraints

- `x` has at most 10 000 entries.
- Plain Python only: use the `rng` you are given, not the `random` module's global functions.

## Hints

1. At train time a unit survives with probability `1 - p`. What is the expected value of `x_i` times a keep-or-drop mask, and how far is it from `x_i`?
2. What single factor, applied to the survivors, brings that expected value back to `x_i`?
3. Where does the scaling happen in inverted dropout: at train time, at eval time, or both? What does that mean for the eval branch?
4. Why must the eval branch not call `rng.random()`, and why would a test notice if it did?

## Explain-back

- Why is dropout switched off at inference? What would predictions look like if you left it on, and what does `model.eval()` do in PyTorch?
- Does dropout change the expected activation of a unit? Show why the `1 / (1 - p)` factor answers that question.
- The original paper scaled weights by `1 - p` at test time instead. Why do frameworks prefer scaling at train time?
- Your model has not yet fit its training set. Should you add dropout now? What should you check first?
