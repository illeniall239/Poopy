# Expected initial loss

Topic: 9. Initialization and activation/gradient statistics
Difficulty: 1 of 3

## Problem

The first number a training run prints is its first sanity check. A freshly initialized classifier knows nothing, so it should spread its probability evenly over the `C` classes, and its cross-entropy should be about `−log(1/C)`. Write two NumPy functions.

- `expected_initial_ce(num_classes)` returns `−log(1/C)` as a Python `float`. Raise `ValueError` if `num_classes < 2`.
- `too_confident_at_init(logits, tol)` checks a batch of initial logits, shape `(N, C)`, before any training. No targets are given: at init the label is unrelated to the logits, so for each row use the cross-entropy **averaged over all `C` possible labels**:

  ```
  row_loss = logsumexp(row) − mean(row)
  ```

  Return `True` if the mean of `row_loss` over the `N` rows is greater than `expected_initial_ce(C) + tol`, else `False` (a Python `bool`). Equal logits give exactly `log C`; the more spread out a row's logits, the higher its loss.

  Compute `logsumexp` stably: logits of size `±1000` must not overflow. Raise `ValueError` if `logits` is not 2-D, if `N == 0`, if `C < 2`, or if `tol < 0`.

## Examples

```
expected_initial_ce(10)   → 2.302585092994046      log 10
expected_initial_ce(2)    → 0.6931471805599453
expected_initial_ce(1)    → ValueError

too_confident_at_init(np.zeros((4, 10)), 0.1)          → False    loss is exactly log 10
too_confident_at_init(np.array([[0.0, 4.0]]), 0.5)     → True     4.018 − 2 = 2.018 > 0.693 + 0.5
too_confident_at_init(np.array([[0.0, 0.2]]), 0.5)     → False    0.703 < 1.193
too_confident_at_init(np.array([[1000.0, -1000.0]]), 1.0) → True  loss is 1000
```

## Constraints

- NumPy only.
- `N` up to 100 000, `C` up to 10 000.

## Hints

1. If the model gives every class the same probability, what is that probability, and what is `−log` of it?
2. For one row and one label `y`, cross-entropy is `logsumexp(row) − row[y]`. What do you get when you average that over all `C` choices of `y`?
3. Why can that average never be below `log C`? When is it exactly `log C`?
4. How does subtracting the row maximum keep `logsumexp` from overflowing while giving the same answer?

## Explain-back

- Your 10-class network's first loss is 27. What does that tell you about the output layer, and what would you change before training?
- "It will come down anyway." Why is a far-too-high initial loss still a problem? Where do the first training steps go?
- Why does scaling the last layer's weights down (or zeroing its bias) bring the initial loss back to about `log C`?
- Why is zeroing *all* the weights not the fix, even though it gives exactly `log C`?
