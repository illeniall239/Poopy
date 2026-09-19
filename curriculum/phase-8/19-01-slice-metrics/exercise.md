# Slice metrics and worst errors

Topic: 19. Error analysis and project strategy
Difficulty: 1 of 3

## Problem

One overall score hides where a model fails. Write two pure-Python functions for error analysis:

- `slice_metrics(y_true: list, y_pred: list, feature_values: list, metric) -> list[tuple]` groups the rows by the value of one feature (`feature_values[j]` belongs to row `j`, any hashable value), computes `metric(slice_true, slice_pred)` on each slice's lists, and returns a list of `(value, score, support)` tuples, where `support` is the number of rows in the slice. `metric` is higher-is-better (accuracy, F1), so sort worst first: ascending by score. Slices with equal scores keep the order in which their value first appears in `feature_values`. Raise `ValueError` if the lists are empty or of different lengths.
- `worst_errors(y_true: list[int], scores: list[float], n: int) -> list[int]` finds the most confident mistakes of a binary classifier. `scores[j]` is the predicted probability that row `j` is class 1; the predicted label is 1 when `score >= 0.5`, else 0. A mistake is a row whose predicted label differs from `y_true[j]`; its confidence is `|score - 0.5|`. Return the indices of up to `n` mistakes, most confident first, lower index first on ties. Raise `ValueError` if the lengths differ or `n < 0`.

## Examples

```
acc = lambda t, p: sum(a == b for a, b in zip(t, p)) / len(t)
slice_metrics([1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 1, 1], ["web", "web", "app", "app", "app", "web"], acc)
    → [("app", 0.3333, 3), ("web", 1.0, 3)]
worst_errors([1, 0, 1, 0, 1], [0.05, 0.4, 0.45, 0.98, 0.9], 2)
    → [3, 0]      row 3: predicted 1 at 0.98 (confidence 0.48); row 0: predicted 0 at 0.05 (0.45)
worst_errors([1, 0], [0.9, 0.1], 5)  → []      no mistakes
```

## Constraints

- Pure Python, no numpy.
- Up to 1 000 000 rows; call `metric` once per slice.
- Scores returned exactly as `metric` returns them.

## Hints

1. How do you collect each slice's `y_true` and `y_pred` lists in one pass while remembering the order the values first appeared?
2. Python's `sorted` is stable. What does that give you for free if the slices are already in first-appearance order?
3. For `worst_errors`, which rows do you discard before sorting, and what does a score of exactly 0.5 predict?
4. What single sort key puts "most confident first, lower index on ties"?

## Explain-back

- The model is 90% accurate overall and 55% accurate on one slice. How can both be true, and what would you do next?
- Why are the most confident mistakes worth reading by hand? What do you often find there besides model errors?
- After reading 100 errors you count 40 blurry images and 8 rare-accent cases. The accents are harder and more interesting. Which do you fix first, and why?
- A slice has a support of 4 and an accuracy of 0.25. How much weight does that deserve, and how would you decide?
