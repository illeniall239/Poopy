# Weighted cross-entropy from logits

Topic: 5. Loss functions for nets
Difficulty: 2 of 3

## Problem

Write `weighted_ce(logits, target, class_weights=None, reduction="mean")` in NumPy (no torch), reproducing PyTorch's `F.cross_entropy(logits, target, weight=class_weights, reduction=reduction)`.

- `logits`: raw, unnormalised scores, shape `(N, C)` (a 2-D NumPy array or nested list): one row per example, one column per class. They are **not** probabilities; do not expect them to be softmaxed already.
- `target`: `N` integer class indices, each in `0 … C − 1`.
- `class_weights`: `C` non-negative floats, or `None` for all ones.
- `reduction`: `"mean"` or `"sum"`.

For example `i` with true class `y = target[i]`, the loss is `w[y] · (logsumexp(logits[i]) − logits[i, y])`, which is `−w[y] · log softmax(logits[i])[y]`. Compute `logsumexp` stably by subtracting the row maximum first: no NumPy overflow, divide or invalid warning may occur even for logits of `±1000`.

- `"sum"` returns the sum of the per-example losses.
- `"mean"` returns the **weighted** mean, the way PyTorch does it: the sum of the per-example losses divided by the sum of the weights of the examples' true classes, `Σ w[target[i]]`. Without class weights that is just the average over `N`.

Return a Python `float`. Raise `ValueError` if `logits` is not 2-D or has no rows or no columns, `target` has the wrong length or an index out of range, `class_weights` has the wrong length or a negative entry, `reduction` is anything else, or the reduction is `"mean"` and `Σ w[target[i]]` is 0.

## Examples

```
weighted_ce([[0.0, 0.0]], [0])                                   → 0.6931471805599453   log 2
weighted_ce([[2.0, 0.0, -1.0], [0.5, 0.5, 3.0]], [0, 2])         → 0.1609272...
weighted_ce([[2.0, 0.0, -1.0], [0.5, 0.5, 3.0]], [0, 2], reduction="sum")
                                                                 → 0.3218544...         twice the mean
weighted_ce([[0.0, 0.0], [0.0, 0.0]], [0, 1], [1.0, 3.0])        → 0.6931471805599453   (1·log2 + 3·log2) / (1 + 3)
weighted_ce([[0.0, 0.0], [0.0, 0.0]], [0, 1], [1.0, 3.0], "sum") → 2.772588722239781    4 · log 2
weighted_ce([[0.0, 0.0], [0.0, 0.0]], [1, 1], [1.0, 3.0])        → 0.6931471805599453   (3·log2 + 3·log2) / (3 + 3)
weighted_ce([[1000.0, -1000.0]], [1])                            → 2000.0
```

## Constraints

- `N` up to 10 000, `C` up to 1 000.
- NumPy, vectorised; no torch.
- Matches PyTorch within `1e-9` on float64 inputs.

## Hints

1. Write `log softmax(z)[y]` in terms of `z[y]` and a log of a sum of exponentials. Which part can overflow, and what constant can you subtract from every logit without changing the result?
2. How do you pick out `logits[i, target[i]]` for every row at once with NumPy indexing?
3. For `"mean"` with class weights, what do you divide by: `N`, `C`, the sum of all class weights, or something else? Try the fourth example by hand.
4. If you switch from `"mean"` to `"sum"`, by what factor does the loss (and therefore every gradient) grow for an unweighted batch of `N` examples?

## Explain-back

- PyTorch's `cross_entropy` takes logits. What happens to the loss and its gradients if you apply softmax first and pass probabilities in (a "double softmax")?
- You switch a training script from `reduction="mean"` to `"sum"` with batch size 128 and keep the learning rate. What just happened to the effective step size?
- Why does the weighted mean divide by `Σ w[target[i]]` rather than by `N`? What would an up-weighted rare class do to the loss scale otherwise?
- Accuracy is what you report. Why can't you train on it directly?
