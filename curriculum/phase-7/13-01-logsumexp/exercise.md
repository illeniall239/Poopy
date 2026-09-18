# Log-sum-exp

Topic: 13. Likelihood, entropy and cross-entropy
Difficulty: 2 of 3

## Problem

Write three functions in pure Python (no NumPy; `math` allowed):

- `logsumexp(xs: list[float]) -> float` — `log(Σ exp(xᵢ))`, computed stably: subtract the maximum before exponentiating and add it back. Must return `1000 + log 2` for `[1000, 1000]` and `-1000 + log 2` for `[-1000, -1000]` without overflow or underflow. Raise `ValueError` on an empty list.
- `log_softmax(xs: list[float]) -> list[float]` — `xᵢ - logsumexp(xs)` for every entry; the exponentials of the result sum to 1.
- `softmax(xs: list[float]) -> list[float]` — `exp` of `log_softmax`, so it is stable for the same inputs.

## Examples

```
logsumexp([0.0, 0.0])            → 0.6931...        log 2
logsumexp([1000.0, 1000.0])      → 1000.6931...
logsumexp([-1000.0, -1000.0])    → -999.3068...
logsumexp([5.0])                 → 5.0
log_softmax([1.0, 2.0, 3.0])     → [-2.4076, -1.4076, -0.4076]
softmax([1.0, 2.0, 3.0])         → [0.0900, 0.2447, 0.6652]
softmax([1000.0, 0.0])           → [1.0, 0.0]        no OverflowError
softmax([1.0, 1.0, 1.0])         → [1/3, 1/3, 1/3]
```

## Constraints

- Up to 100 000 entries; two passes (max, then sum).
- Must match the naive formula `math.log(sum(math.exp(x) for x in xs))` within `1e-12` on moderate inputs, and match NumPy on random inputs.
- `softmax` entries sum to 1 within `1e-12` and are all in `[0, 1]`.

## Hints

1. `exp(1000)` overflows to `inf`. Factor `exp(m)` out of the sum with `m = max(xs)`: what is left inside the sum, and what is the largest value inside it?
2. After subtracting the max, what is the smallest possible value of the sum? Can `log` of it ever be `-inf`?
3. `log_softmax` is one subtraction per entry once you have `logsumexp`. Why compute it this way rather than `log(softmax(x))`?
4. Check `softmax([1000, 0])` by hand after the shift: which entries become `exp(0)` and `exp(-1000)`?

## Explain-back

- Why does subtracting a constant from every logit leave `softmax` unchanged? Show it algebraically in one line.
- `log(softmax(x))` computed as two steps gives `log(0) = -inf` for a logit of `-1000` in the presence of a `0`. Why does `log_softmax` avoid that, and where in a loss function does this matter?
- Adding 1000 to every entry of `xs` changes `logsumexp` by how much? Why is that a useful sanity check?
- Cross-entropy with a one-hot target is `-log_softmax(x)[target]`. Why is this the natural loss for a classifier's logits, and what happens to the gradient if you clip probabilities at `1e-7` instead?
