# Softmax cross-entropy backward

Topic: 6. Vectorized backprop: tensors and the backprop ninja
Difficulty: 2 of 3

## Problem

Write `softmax_ce_backward(logits, targets)` in NumPy, for a batch.

- `logits` has shape `(N, C)`: one row of raw scores per example, `C` classes.
- `targets` has shape `(N,)`: the integer class index of each example, in `0 … C−1`.

Return the tuple `(loss, dlogits)`:

- `loss` — the **mean** over the batch of the cross-entropy `−log softmax(logits[n])[targets[n]]`, as a Python `float`.
- `dlogits` — the gradient of that mean loss with respect to `logits`, a NumPy array of shape `(N, C)`. Compute it directly from the closed form (softmax probabilities minus the one-hot targets, divided by `N`), not by finite differences.

Both must be numerically stable: logits of size `±1000` must not produce `inf`, `nan` or a NumPy overflow warning. Do not modify the inputs.

Raise `ValueError` if `logits` is not 2-D, if `N == 0`, if `targets` does not have shape `(N,)`, or if any target is outside `0 … C−1`.

NumPy only: do not use torch in your solution (the tests use `torch.autograd` to check you).

## Examples

```
softmax_ce_backward([[0, 0]], [0])        → (0.6931471805599453, [[-0.5, 0.5]])
softmax_ce_backward([[0, 0], [0, 0]], [0, 1])
                                          → (0.6931471805599453, [[-0.25, 0.25], [0.25, -0.25]])
softmax_ce_backward([[1000, 0]], [1])     → (1000.0, [[1.0, -1.0]])
```

## Constraints

- NumPy only, vectorized.
- `N` up to 10 000, `C` up to 1000.
- Loss and gradient match `torch.nn.functional.cross_entropy` + `.backward()` within `1e-9` on float64.

## Hints

1. What does subtracting each row's maximum do to the softmax, and why is it allowed?
2. How can you write `log softmax` so you never take the log of a number that might have rounded to 0?
3. Differentiate `−log softmax(z)[y]` with respect to `z[j]` for `j == y` and for `j != y`. Can both cases be written as one expression involving a one-hot vector?
4. The loss is a mean over `N` examples. What does that do to each example's gradient row? How can you build the one-hot subtraction with fancy indexing instead of a loop?

## Explain-back

- Each row of `dlogits` sums to zero. Why must it, and what does it mean for the logits of the wrong classes?
- Where does the `1/N` come from? What happens to the effective learning rate if the loss divides by `N` but the gradient does not (or the other way round)?
- Why is combining softmax and cross-entropy into one backward step better, numerically and in effort, than backpropagating through each separately?
- How would you convince yourself this gradient is right if you had no torch to compare with?
