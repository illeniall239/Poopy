# Bias, variance or mismatch

Topic: 19. Error analysis and project strategy
Difficulty: 1 of 3

## Problem

Five error rates, measured on five sets, tell you what to work on next. Write one pure-Python function:

`diagnose(human: float, train: float, train_dev: float, dev: float, test: float) -> str`

The arguments are error rates as fractions in `[0, 1]`: human-level error (a proxy for the lowest achievable error), training error, train-dev error (held-out rows drawn from the training distribution), dev error and test error. Compute four gaps:

| Gap | Formula | Returned name |
|---|---|---|
| avoidable bias | `train - human` | `"avoidable bias"` |
| variance | `train_dev - train` | `"variance"` |
| data mismatch | `dev - train_dev` | `"data mismatch"` |
| dev overfitting | `test - dev` | `"dev overfitting"` |

Return the name of the largest gap. Gaps within `1e-9` of each other count as equal, and ties go to the earlier row of the table. A negative gap is allowed; it is simply small. Raise `ValueError` if any argument is outside `[0, 1]`.

## Examples

```
diagnose(0.01, 0.08, 0.09, 0.10, 0.10)   → "avoidable bias"    7 points above human level
diagnose(0.01, 0.015, 0.08, 0.09, 0.09)  → "variance"
diagnose(0.01, 0.015, 0.02, 0.10, 0.10)  → "data mismatch"
diagnose(0.01, 0.02, 0.03, 0.04, 0.12)   → "dev overfitting"
diagnose(0.2, 0.3, 0.4, 0.4, 0.4)        → "avoidable bias"    ties with variance (0.1 each, up to rounding)
diagnose(0.01, 0.08, 0.09, 0.10, 1.2)    → ValueError
```

## Constraints

- Pure Python.
- Compare gaps with the `1e-9` tolerance, not with `==`.

## Hints

1. Which two sets differ only in whether the model trained on them, and which two differ only in their distribution?
2. Why is it the train-dev set, not the dev set, that separates variance from data mismatch?
3. `0.4 - 0.3` and `0.3 - 0.2` look equal. Are they equal in floating point, and how should "largest" be decided when they are nearly equal?
4. If you keep a running best and walk the gaps in table order, what comparison makes an earlier gap win a tie?

## Explain-back

- Training error is 8% and human error is 1%. Your manager wants to collect ten times more data. What do you say, and what would you try instead?
- Why does a large gap between train-dev and dev error mean more of the same training data will not fix the problem?
- Test error is far above dev error. What happened to the dev set, and what do you do about it?
- Before tuning anything, you find that 15% of the dev labels are wrong. How does that change this diagnosis?
