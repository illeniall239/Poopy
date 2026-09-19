# Early stopping

Topic: 11. Regularization in deep nets
Difficulty: 1 of 3

## Problem

Early stopping watches the **validation** loss after every epoch and stops once it has not improved for `patience` epochs in a row, then restores the weights from the best epoch. Write `early_stopping_epoch(val_losses, patience)` in plain Python.

- `val_losses[i]` is the validation loss after epoch `i` (epochs are numbered from `0`).
- Walk the epochs in order, tracking the best (lowest) loss so far. An epoch **improves** only if its loss is strictly lower than the best so far; equal is not an improvement. The first epoch always improves.
- Count consecutive epochs without improvement. As soon as that count reaches `patience`, training stops: return the index of the best epoch, the one whose weights you would restore. Epochs after the stop are never looked at.
- If the run ends before the count ever reaches `patience`, return `None`: training never stalled.

Raise `ValueError` if `patience < 1`. An empty list returns `None`.

## Examples

```
early_stopping_epoch([1.0, 0.8, 0.7, 0.75, 0.72, 0.71], 3)  → 2      three epochs without beating 0.7
early_stopping_epoch([1.0, 0.8, 0.7, 0.75, 0.72, 0.71], 4)  → None   ran out of epochs first
early_stopping_epoch([0.5, 0.5, 0.5], 2)                     → 0      ties do not count as improvement
early_stopping_epoch([1.0, 0.9, 0.95, 0.96, 0.5], 2)         → 1      stops at epoch 3, never sees 0.5
early_stopping_epoch([], 3)                                  → None
```

## Constraints

- At most 10 000 epochs; losses are finite floats.
- Plain Python only.

## Hints

1. What three things do you need to remember as you walk the list?
2. What happens to the "epochs without improvement" counter when an epoch does improve?
3. Should the check "has the counter reached `patience`?" happen before or after you update it for the current epoch?
4. Why must you return the best epoch rather than the epoch where you stopped?

## Explain-back

- Why does early stopping watch the validation loss and not the training loss?
- Why restore the best epoch's weights instead of keeping the last ones?
- The training loss is still high and falling when early stopping triggers. What does that tell you, and what would you change?
- How does the choice of `patience` trade off wasted compute against stopping on a noisy blip?
