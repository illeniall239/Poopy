# Label smoothing

Topic: 5. Loss functions for nets
Difficulty: 1 of 3

## Problem

A one-hot target tells the network to put probability 1 on the right class, which it can only approach by growing its logits without limit. Label smoothing softens the target: take `eps` of the probability mass away from the one-hot vector and spread it **uniformly over all `k` classes** (the true class included).

Write `label_smoothed_targets(k, target, eps)` in plain Python (no numpy, no torch). It returns a list of `k` floats:

- every class gets `eps / k`;
- the `target` class additionally gets `1 − eps`, so it holds `1 − eps + eps / k`.

The list sums to 1 (within `1e-12`), and for `eps < 1` the `target` class is still the unique largest entry. This is the convention PyTorch uses for `cross_entropy(..., label_smoothing=eps)`: cross-entropy against your targets must equal PyTorch's smoothed loss.

Raise `ValueError` if `k < 2`, `target` is not in `0 … k − 1`, or `eps` is not in `[0, 1)`.

## Examples

```
label_smoothed_targets(4, 2, 0.0)   → [0.0, 0.0, 1.0, 0.0]       plain one-hot
label_smoothed_targets(4, 2, 0.1)   → [0.025, 0.025, 0.925, 0.025]
label_smoothed_targets(2, 0, 0.2)   → [0.9, 0.1]
label_smoothed_targets(3, 3, 0.1)   → ValueError                 no class 3
label_smoothed_targets(3, 0, 1.0)   → ValueError
```

## Constraints

- `k` up to 100 000.
- Plain Python only.

## Hints

1. Before any smoothing, what does the target vector look like, and what does it sum to?
2. If you give `eps / k` to every one of the `k` classes, how much mass have you handed out? How much is left for the one-hot part?
3. Some write-ups spread `eps` over the other `k − 1` classes only. How would the numbers differ, and which convention does the Problem ask for?
4. Why must `eps` stay below 1 for the target to remain the argmax? What happens at exactly `eps = 1`?

## Explain-back

- After smoothing, is the target class still the one the model should predict? What exactly changes about what the model is pushed toward?
- With a smoothed target, the loss can no longer reach 0. What does the network stop doing to its logits, and why is that a regularizer?
- If you apply softmax to your logits and then pass them to a loss that expects logits (like PyTorch's `cross_entropy`), what goes wrong? Does label smoothing fix or hide it?
