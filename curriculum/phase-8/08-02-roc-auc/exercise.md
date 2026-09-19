# ROC AUC with ties

Topic: 8. Classification metrics
Difficulty: 2 of 3

## Problem

AUC is the probability that a randomly chosen positive gets a higher score than a randomly chosen negative, with a tie counting as one half. Write three pure-Python functions. `y_true` holds labels `0` and `1`, `scores` holds floats (higher means "more positive").

- `roc_auc(y_true: list[int], scores: list[float]) -> float` — the **rank (Mann–Whitney) formulation**:
  1. rank all scores in ascending order from 1 to n; tied scores all get the **average** of the ranks they span (scores `[5, 7, 7, 9]` get ranks `[1, 2.5, 2.5, 4]`);
  2. with `R₊` the sum of the positives' ranks, `AUC = (R₊ − n₊(n₊ + 1)/2) / (n₊ · n₋)`.
- `roc_curve(y_true: list[int], scores: list[float]) -> tuple[list[float], list[float]]` — returns `(fpr, tpr)`. The first point is `(0.0, 0.0)`. Then, for each **distinct** score taken as a threshold in descending order, predict positive when `score >= threshold` and append that threshold's false positive rate and true positive rate. Tied scores therefore move the curve diagonally in a single step. The last point is `(1.0, 1.0)`.
- `auc_trapezoid(fpr: list[float], tpr: list[float]) -> float` — the area under the polyline through the points, by the trapezoid rule.

`auc_trapezoid(*roc_curve(y, s))` must equal `roc_auc(y, s)` (within `1e-12`), ties included.

Raise `ValueError` from `roc_auc` and `roc_curve` if the lists are empty or differ in length, if a label is not 0 or 1, or if either class is missing (AUC is undefined then).

## Examples

```
roc_auc([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8])   → 0.75      3 of the 4 (pos, neg) pairs are ordered right
roc_auc([0, 1], [0.5, 0.5])                     → 0.5       a tie counts one half
roc_auc([1, 1, 0, 0], [0.3, 0.3, 0.3, 0.3])     → 0.5       constant scores carry no information
roc_curve([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8])  → ([0.0, 0.0, 0.5, 0.5, 1.0], [0.0, 0.5, 0.5, 1.0, 1.0])
auc_trapezoid([0.0, 0.0, 0.5, 0.5, 1.0], [0.0, 0.5, 0.5, 1.0, 1.0])   → 0.75
roc_auc([1, 1], [0.2, 0.9])                     → ValueError  no negatives
```

## Constraints

- Pure Python: `math` is allowed, numpy is not.
- Up to 100 000 rows; `roc_auc` and `roc_curve` are O(n log n) (comparing every positive with every negative is O(n²) and too slow).
- Random scores on a large sample give an AUC near 0.5.

## Hints

1. Before ranks: how would you compute AUC by comparing pairs? Why does that cost too much at 100 000 rows?
2. After sorting, a run of equal scores occupies positions `i` through `j`. What single rank should every member of the run get so that no positive or negative gains from the tie?
3. Why does subtracting `n₊(n₊ + 1)/2` from the positives' rank sum leave exactly the number of (positive, negative) pairs the positives win?
4. In `roc_curve`, what goes wrong if you add one point per row instead of one per distinct score when several rows share a score?

## Explain-back

- A model has AUC 0.95. Does that tell you which threshold to use? What does AUC measure and what does it not?
- Why must ties count one half? What AUC would a model with constant scores get if ties were ignored, and why is that a lie?
- On a data set with 0.1% positives, why can the ROC curve look excellent while the precision–recall curve looks poor?
- An AUC of 0.2 on a validation set. What does that suggest about the model or the labels?
