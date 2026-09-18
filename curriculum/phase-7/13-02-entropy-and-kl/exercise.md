# Entropy, cross-entropy and KL divergence

Topic: 13. Likelihood, entropy and cross-entropy
Difficulty: 2 of 3

## Problem

Write three functions over probability lists in pure Python (no NumPy; `math` allowed), all in nats (natural log):

- `entropy(p: list[float]) -> float` — `H(p) = -Σ pᵢ log pᵢ`, with the convention `0 · log 0 = 0`.
- `cross_entropy(p: list[float], q: list[float]) -> float` — `H(p, q) = -Σ pᵢ log qᵢ`. Terms with `pᵢ = 0` contribute 0 regardless of `qᵢ`. If some `pᵢ > 0` while `qᵢ = 0`, return `math.inf`.
- `kl(p: list[float], q: list[float]) -> float` — `KL(p ‖ q) = Σ pᵢ log(pᵢ / qᵢ) = H(p, q) - H(p)`, same conventions, `inf` when `q` has a zero where `p` does not.

All three validate their inputs: raise `ValueError` if a list is empty, any entry is negative, the entries do not sum to 1 within `1e-9`, or (for the two-argument functions) the lengths differ.

## Examples

```
entropy([0.5, 0.5])                 → 0.6931...     log 2: one bit of surprise
entropy([1.0, 0.0])                 → 0.0           nothing to learn
entropy([0.25] * 4)                 → 1.3862...     log 4
cross_entropy([1.0, 0.0], [0.9, 0.1])   → 0.1053...   -log 0.9
cross_entropy([1.0, 0.0], [0.0, 1.0])   → inf
kl([0.5, 0.5], [0.5, 0.5])          → 0.0
kl([0.5, 0.5], [0.9, 0.1])          → 0.5108...
kl([0.9, 0.1], [0.5, 0.5])          → 0.3681...     not the same: KL is asymmetric
kl([1.0, 0.0], [0.5, 0.5])          → 0.6931...
entropy([0.6, 0.6])                 → ValueError
```

## Constraints

- Up to 100 000 categories.
- Must match NumPy formulas within `1e-12`; `kl` must equal `cross_entropy(p, q) - entropy(p)` within `1e-12` and be `>= 0` for every random pair.
- `entropy` is maximal for the uniform distribution of the same length.

## Hints

1. `math.log(0)` raises. Which terms of the entropy sum have `pᵢ = 0`, and what should they contribute? How do you skip them?
2. In `cross_entropy`, two different zeros can appear: `pᵢ = 0` and `qᵢ = 0`. Which one is harmless and which one means "the model said impossible to something that happened"?
3. `kl(p, q)` can be built from the other two functions. Which subtraction, and does it still give `inf` correctly?
4. Try `kl([0.5, 0.5], [0.9, 0.1])` and the reverse by hand. Which direction penalizes "q puts little mass where p has a lot"?

## Explain-back

- Why is cross-entropy asymmetric? In `cross_entropy(targets, predictions)`, which argument is the model's output, and what goes wrong if you swap them?
- `entropy([1.0, 0.0])` is 0. Someone claims a deterministic outcome has entropy 1 "because you know it for sure". What is entropy actually measuring?
- KL is never negative. What does `kl(p, q) = 0` tell you about `p` and `q`? And what does minimizing `cross_entropy(p, q)` over `q` do, given that `entropy(p)` is fixed?
- Why do libraries compute the classification loss from logits with `log_softmax` rather than calling your `cross_entropy` on `softmax` outputs?
