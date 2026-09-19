# Stable softmax and top-k accuracy

Topic: 9. Multiclass: softmax regression and categorical cross-entropy
Difficulty: 1 of 3

## Problem

Write two NumPy functions.

- `softmax(logits: np.ndarray) -> np.ndarray` — softmax along the **last** axis, so a 1-D vector gives one distribution and a 2-D `(n, C)` array gives one distribution per row. Output has the same shape, every entry is in `[0, 1]`, and each distribution sums to 1 (within `1e-12`). Subtract each row's maximum before exponentiating: softmax is unchanged by adding a constant to every logit, and after the shift the largest exponent is `e⁰ = 1`, so nothing overflows. It must not trigger any NumPy overflow, divide or invalid warning, even on `[1000, 1001]`.
- `top_k_accuracy(logits_rows: np.ndarray, targets: np.ndarray, k: int) -> float` — `logits_rows` has shape `(n, C)` and `targets` holds `n` class indices. A row counts as correct when its target is among the `k` highest-scoring classes of that row. Return the fraction of correct rows as a Python `float`.
  - Ties inside a row are broken by the **smaller class index**: order the classes by logit descending, then by index ascending, and take the first `k`. (Equivalently: the target's rank is the number of classes with a strictly larger logit plus the number with an equal logit and a smaller index; it is in the top `k` when that rank is below `k`.)
  - Work from the logits directly: softmax does not change which classes are largest.
  - Raise `ValueError` if `logits_rows` is not 2-D, `len(targets) != n`, `k < 1` or `k > C`, or a target is outside `0..C−1`.

## Examples

```
softmax(np.array([1000.0, 1001.0]))     → [0.26894142, 0.73105858]
softmax(np.array([1.0, 2.0, 3.0]))      → [0.09003057, 0.24472847, 0.66524096]
softmax(np.array([[0.0, 0.0], [0.0, np.log(3)]]))   → [[0.5, 0.5], [0.25, 0.75]]
top_k_accuracy(np.array([[0.1, 0.5, 0.4], [0.9, 0.05, 0.05]]), np.array([2, 0]), k=1)  → 0.5
top_k_accuracy(np.array([[0.1, 0.5, 0.4], [0.9, 0.05, 0.05]]), np.array([2, 0]), k=2)  → 1.0
top_k_accuracy(np.array([[1.0, 1.0, 0.0]]), np.array([1]), k=1)   → 0.0   tie goes to class 0
```

## Constraints

- NumPy allowed, vectorized over rows: no Python loop over the `n` rows in `softmax`.
- `n` up to 100 000, `C` up to 1000 for `softmax`; `top_k_accuracy` may loop over rows only if it stays within a second at `n = 10 000`, `C = 10`.
- Probabilities within `1e-12` of an exact computation.

## Hints

1. Show that `softmax(z + c) = softmax(z)` for any constant `c`. Which `c` makes the largest exponent exactly 1?
2. For a 2-D input, the maximum and the sum must be taken per row. What does `keepdims=True` do for the broadcasting?
3. Is `softmax(z / T)` the same as `softmax(z)`? What does a temperature `T` below 1 do to the distribution, and why can `T` not be 0?
4. For top-k with ties, how do you count how many classes beat the target under the "larger logit, or equal logit and smaller index" rule without sorting the whole row?

## Explain-back

- Why does `np.exp(1001)` overflow while softmax of `[1000, 1001]` is a perfectly ordinary distribution?
- Can argmax over the logits and argmax over the softmax probabilities ever disagree? Why?
- Softmax is shift-invariant but not scale-invariant. What does that say about temperature?
- A PyTorch model ends in `nn.Softmax` and is trained with `nn.CrossEntropyLoss`. What goes wrong, and what is the fix?
