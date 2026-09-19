# Early stopping and diagnosis

Topic: 6. Overfitting, bias–variance and regularization
Difficulty: 2 of 3

## Problem

Write two pure-Python functions that read loss curves (one loss per epoch, index 0 is the first epoch).

`early_stopping_epoch(val_losses: list[float], patience: int) -> int` replays training with early stopping and returns the epoch whose weights you would keep:

- Walk the epochs in order, tracking the best validation loss so far. An epoch **improves** only if its loss is strictly lower than the best so far (equal does not count).
- After each epoch without improvement, count it. When `patience` consecutive epochs have passed without improvement, training stops there: return the index of the best epoch seen up to that point. Epochs after the stop are never looked at, even if one of them is lower.
- If the curve ends before patience runs out, return the index of the best epoch overall (the first one, if the best value repeats).
- Raise `ValueError` if `val_losses` is empty or `patience < 1`.

`diagnose(train_losses: list[float], val_losses: list[float], target_loss: float, max_gap: float) -> str` reads the **final** epoch of each curve and returns one of three strings, checked in this order:

1. `"underfit"` if the final training loss is above `target_loss`: the model cannot even fit the data it trains on.
2. `"overfit"` if the final validation loss minus the final training loss is above `max_gap`.
3. `"ok"` otherwise.

Raise `ValueError` if either list is empty or their lengths differ.

## Examples

```
early_stopping_epoch([5, 4, 3, 3.5, 3.2, 3.1, 2.0], patience=3)   → 2   stops at epoch 5, never sees the 2.0
early_stopping_epoch([5, 4, 3, 3.5, 2.5, 2.4], patience=2)        → 5   one bad epoch is not enough to stop
early_stopping_epoch([3, 2, 2, 2], patience=5)                    → 1   ran out of data; ties keep the first
diagnose([2.0, 1.5], [2.1, 1.6], target_loss=0.5, max_gap=0.2)   → "underfit"
diagnose([1.0, 0.1], [1.1, 0.9], target_loss=0.5, max_gap=0.2)   → "overfit"
diagnose([1.0, 0.3], [1.1, 0.4], target_loss=0.5, max_gap=0.2)   → "ok"
```

## Constraints

- Pure Python, no imports needed.
- Up to 100 000 epochs; one pass, O(n).

## Hints

1. What two pieces of state do you need to carry from one epoch to the next?
2. When an epoch improves, what happens to the count of epochs without improvement?
3. Why would returning the index of the minimum of the whole list be wrong, when a real training run would have stopped earlier?
4. For `diagnose`, why must the underfit check come before the gap check? What does a small gap mean when both losses are high?

## Explain-back

- Why does early stopping need a patience window instead of stopping at the first epoch where validation loss goes up?
- Why do you keep the best epoch's weights rather than the weights at the epoch where you stopped?
- Training loss is tiny and validation loss is large. Is that a success? Name two things to try.
- The diagnosis says "underfit". Would adding L2 regularization help? What would?
