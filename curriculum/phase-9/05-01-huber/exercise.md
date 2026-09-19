# Huber loss and its gradient

Topic: 5. Loss functions for nets
Difficulty: 1 of 3

## Problem

Huber loss is a regression loss that behaves like squared error for small residuals and like absolute error for large ones, so a few outliers cannot dominate the gradient. For a residual `r = yhat − y` and a threshold `delta > 0`:

```
huber_one(r) = 0.5 · r²                       if |r| ≤ delta
             = delta · (|r| − 0.5 · delta)    otherwise
```

Write two functions in plain Python (no numpy, no torch):

- `huber(y, yhat, delta=1.0)` returns the **mean** of `huber_one` over all elements, as a float. `y` holds the targets and `yhat` the predictions, both lists of floats of the same length.
- `huber_grad(y, yhat, delta=1.0)` returns the gradient of that mean loss with respect to each `yhat[i]`, as a list of floats the same length as `yhat`. Inside the band it is `r / n`; outside it is `delta · sign(r) / n`, where `n` is the number of elements. At exactly `|r| = delta` both formulas agree, so either is fine.

This is the same loss as PyTorch's `torch.nn.HuberLoss(delta=delta)` with the default mean reduction, and your values must match it within `1e-9`.

Raise `ValueError` if the lists are empty, have different lengths, or `delta ≤ 0`.

## Examples

```
huber([0.0], [0.5])                         → 0.125      inside the band: 0.5 · 0.25
huber([0.0], [3.0])                         → 2.5        outside: 1 · (3 − 0.5)
huber([0.0, 0.0], [0.5, 3.0])               → 1.3125     mean of 0.125 and 2.5
huber([1.0], [-3.0], delta=2.0)             → 6.0        2 · (4 − 1)
huber_grad([0.0, 0.0], [0.5, 3.0])          → [0.25, 0.5]
huber_grad([0.0, 0.0], [-0.5, -30.0])       → [-0.25, -0.5]  the outlier's pull is capped
```

## Constraints

- Lists have 1 to 100 000 elements; values are finite floats.
- Plain Python only.

## Hints

1. For one residual, which branch applies, and how does each branch's slope behave as `|r|` grows?
2. Differentiate `0.5 · r²` and `delta · (|r| − 0.5 · delta)` with respect to `yhat` (remember `r = yhat − y`). What happens to `delta` in the second one?
3. Is the loss continuous at `|r| = delta`? Is its slope? Check both formulas at that point.
4. The loss is a mean over `n` elements. Where does that `n` show up in each element's gradient?

## Explain-back

- Compare the gradient an outlier with residual 100 gets under MSE, L1 and Huber (`delta = 1`). Why does that make Huber robust?
- Inside the band Huber is half the squared error. Why the factor `0.5`, and does it matter for training?
- If you switched to a **sum** reduction on a batch of 64, what would happen to every gradient, and what would you have to do to the learning rate to take the same steps?
- Why is Huber, not accuracy or "within 1 unit" rate, the thing you optimize, even if that rate is what you report?
