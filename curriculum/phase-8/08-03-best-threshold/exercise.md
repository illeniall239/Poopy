# Precision–recall curve and the best threshold

Topic: 8. Classification metrics
Difficulty: 3 of 3

## Problem

A model outputs scores; the threshold turns them into decisions, and it is chosen on validation data for the metric the business cares about. Write two pure-Python functions. `y_true` holds labels `0` and `1`, `scores` holds floats, and a row is predicted positive when `score >= threshold`.

- `pr_curve(y_true: list[int], scores: list[float]) -> list[tuple[float, float, float]]` — one `(threshold, precision, recall)` tuple for each **distinct** score, taken as the threshold, in **descending** threshold order. Every threshold predicts at least one row positive, so precision is always defined.
- `best_threshold(y_true: list[int], scores: list[float], metric: str = "f1", min_precision: float | None = None) -> float` — returns one of the scores (a threshold from `pr_curve`):
  - `metric="f1"`: the threshold with the highest F1 = `2·P·R / (P + R)`.
  - `metric="precision_floor"`: among thresholds whose precision is `>= min_precision`, the one with the highest recall. This is the "we can tolerate at most 10% false alarms, catch as many as possible" rule.
  - In both cases, if several thresholds tie on the quantity being maximized, return the **highest** of them (it flags fewer rows for the same result).

Raise `ValueError` if the lists are empty or differ in length, a label is not 0 or 1, there are no positive labels (recall is undefined), `metric` is not one of the two names, `metric="precision_floor"` is given without a `min_precision` in `(0, 1]`, or no threshold reaches the precision floor.

## Examples

```
y = [1, 1, 0, 1, 0, 0], s = [0.9, 0.8, 0.7, 0.6, 0.4, 0.2]
pr_curve(y, s)  → [(0.9, 1.0, 0.333), (0.8, 1.0, 0.667), (0.7, 0.667, 0.667),
                   (0.6, 0.75, 1.0), (0.4, 0.6, 1.0), (0.2, 0.5, 1.0)]
best_threshold(y, s)                                           → 0.6    F1 = 0.857
best_threshold(y, s, "precision_floor", min_precision=0.9)     → 0.8    recall 0.667 at precision 1.0
best_threshold(y, s, "precision_floor", min_precision=0.7)     → 0.6    recall 1.0 at precision 0.75
best_threshold([1, 0, 0], [0.5, 0.5, 0.1])                    → 0.5
best_threshold(y, s, "precision_floor", min_precision=None)    → ValueError
```

## Constraints

- Pure Python, no imports needed.
- Up to 100 000 rows; both functions O(n log n): sort once, then sweep the thresholds keeping running counts. Recounting TP and FP from scratch at every threshold is O(n²).
- Precision and recall within `1e-12` of the exact fractions.

## Hints

1. If you sort rows by score from high to low, what happens to TP and FP each time you lower the threshold past one more row?
2. Several rows share a score. At which point in the sweep is it correct to emit a curve point: after each row, or after the last row of a run of equal scores?
3. As the threshold drops, which of precision and recall can only go up, and which can go either way?
4. Two thresholds reach the same recall above the precision floor. What is different about the rows they flag, and why prefer the higher one?

## Explain-back

- Why pick the threshold on the validation set and never on the test set?
- The team wants higher precision. Why is moving the threshold the first thing to try, before retraining the model?
- When positives are 0.5% of rows, why is the precision–recall curve more honest than the ROC curve?
- A model's scores are well ranked but badly calibrated. Does that change which threshold `best_threshold` picks? Does it change what "score 0.8" means to a user?
