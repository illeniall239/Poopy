# Fairness metrics

Topic: 18. Responsible AI: fairness, bias and privacy
Difficulty: 2 of 3

## Problem

Per-group rates become fairness metrics by comparing the groups. Each function below takes `metrics: dict`, mapping each group to a dict that has at least the keys `"selection_rate"`, `"tpr"` and `"fpr"` (floats; `"tpr"` or `"fpr"` may be `None` when undefined for that group). Other keys are ignored. Write four pure-Python functions:

- `demographic_parity_difference(metrics: dict) -> float`: the largest selection rate minus the smallest.
- `equalized_odds_difference(metrics: dict) -> float`: the larger of two spreads, (max TPR - min TPR) and (max FPR - min FPR). Raise `ValueError` if any group's `"tpr"` or `"fpr"` is `None`: equalized odds is undefined for that group.
- `disparate_impact_ratio(metrics: dict) -> float`: the smallest selection rate divided by the largest. If every selection rate is 0, return `1.0` (nobody is selected in any group, so no group is disadvantaged).
- `passes_four_fifths(metrics: dict) -> bool`: `True` when the disparate-impact ratio is at least 0.8. Allow `1e-9` of floating-point slack, so a ratio that is mathematically exactly 0.8 passes.

All four raise `ValueError` if `metrics` has fewer than two groups.

## Examples

```
m = {"a": {"selection_rate": 0.5, "tpr": 1.0, "fpr": 0.0},
     "b": {"selection_rate": 0.5, "tpr": 0.5, "fpr": 0.5}}
demographic_parity_difference(m) → 0.0
equalized_odds_difference(m)     → 0.5      same selection rate, very different errors
m = {"a": {"selection_rate": 0.5, "tpr": 0.8, "fpr": 0.2},
     "b": {"selection_rate": 0.35, "tpr": 0.7, "fpr": 0.1}}
disparate_impact_ratio(m)        → 0.7
passes_four_fifths(m)            → False
```

## Constraints

- Pure Python, no numpy.
- Results within `1e-9`.

## Hints

1. Each metric compares a rate across groups. Which rate does each one compare, and does it take a difference or a ratio?
2. For equalized odds, why are two spreads computed separately rather than one spread over TPR and FPR together?
3. What should the ratio be when the largest selection rate is 0, and why is dividing anyway a bug?
4. Why is `0.6 / 0.75 >= 0.8` `False` in floating point, and how do you compare with a tolerance?

## Explain-back

- In the first example the model passes demographic parity and fails equalized odds. Which one would you report, and why is "the one that passed" the wrong reason?
- Why can demographic parity and equalized odds not both be satisfied when the groups have different base rates of the positive label?
- A team says "we dropped the gender column, so the model is fair". What does that miss, and what would these metrics show?
- The four-fifths rule passes at 0.81. Does that make the model fair? What does it leave out?
