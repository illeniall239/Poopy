# Per-group metrics

Topic: 18. Responsible AI: fairness, bias and privacy
Difficulty: 1 of 3

## Problem

A fairness audit starts by evaluating the classifier separately for each group. Write one pure-Python function:

`group_metrics(y_true: list[int], y_pred: list[int], groups: list) -> dict`

`y_true` and `y_pred` hold 0 or 1 (1 is the positive outcome, such as "approved"); `groups[j]` is the group of row `j` (any hashable value). Return a dict with one entry per distinct group, mapping it to a dict with exactly these keys:

- `"n"`: the number of rows in the group (an `int`).
- `"selection_rate"`: the fraction of the group's rows predicted 1.
- `"tpr"`: true positive rate, `TP / (TP + FN)`, or `None` if the group has no actual positives.
- `"fpr"`: false positive rate, `FP / (FP + TN)`, or `None` if the group has no actual negatives.
- `"accuracy"`: the fraction of the group's rows where `y_pred == y_true`.

Raise `ValueError` if the three lists are empty or have different lengths.

## Examples

```
y_true = [1, 1, 0, 0, 1, 0, 0, 0]
y_pred = [1, 0, 0, 0, 1, 1, 1, 0]
groups = ["a", "a", "a", "a", "b", "b", "b", "b"]
group_metrics(y_true, y_pred, groups) →
  {"a": {"n": 4, "selection_rate": 0.25, "tpr": 0.5, "fpr": 0.0,    "accuracy": 0.75},
   "b": {"n": 4, "selection_rate": 0.75, "tpr": 1.0, "fpr": 0.6667, "accuracy": 0.5}}
group_metrics([0, 0], [1, 0], ["x", "x"])["x"]["tpr"] → None     no actual positives in "x"
group_metrics([1], [1, 0], ["x"])                      → ValueError
```

## Constraints

- Pure Python, no numpy.
- Up to 1 000 000 rows and 100 groups; one pass over the rows plus work per group.
- Rates within `1e-9`.

## Hints

1. What four counts per group are enough to compute every metric in the list?
2. How can you gather the counts for all groups in a single pass without knowing the groups in advance?
3. Which denominator is the number of actual positives, and which is the number of actual negatives?
4. What does a TPR mean for a group that has no actual positives, and why is `None` more honest than 0 there?

## Explain-back

- Two groups have the same accuracy. Can the model still treat them very differently? Show it with the error types.
- The protected column was dropped before training, but you still need it here. Why, and what does dropping it fail to remove?
- Group "b" has 12 rows. How much would you trust its rates, and what would you report next to them?
- Why is per-group evaluation the first step of a fairness audit rather than the last check before launch?
