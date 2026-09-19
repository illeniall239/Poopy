# Confusion matrix, precision, recall, F1

Topic: 8. Classification metrics
Difficulty: 1 of 3

## Problem

Write three pure-Python functions. Labels can be any hashable, sortable values (ints or strings); `y_true` and `y_pred` are lists of the same non-zero length, otherwise raise `ValueError`.

- `confusion_matrix(y_true: list, y_pred: list, labels: list | None = None) -> list[list[int]]` — a square matrix where `M[i][j]` counts rows whose true label is `labels[i]` and predicted label is `labels[j]` (rows = truth, columns = prediction). If `labels` is `None`, use `sorted(set(y_true) | set(y_pred))`. Raise `ValueError` if a value in either list is not in `labels`.
- `precision_recall_f1(y_true: list, y_pred: list, positive=1) -> tuple[float, float, float]` — treat `positive` as the positive class and everything else as negative.
  - precision = TP / (TP + FP), recall = TP / (TP + FN), F1 = 2·P·R / (P + R).
  - Any 0/0 is defined as `0.0`: a model that never predicts positive has precision `0.0`, not a crash. Same for recall with no actual positives, and F1 when `P + R = 0`.
- `macro_f1(y_true: list, y_pred: list) -> float` — for each label in `sorted(set(y_true) | set(y_pred))`, compute F1 with that label as positive, and return the unweighted mean.

## Examples

```
confusion_matrix([1, 0, 1, 1, 0], [1, 1, 0, 1, 0])   → [[1, 1], [1, 2]]     rows: true 0, true 1
precision_recall_f1([1, 0, 1, 1, 0], [1, 1, 0, 1, 0]) → (0.6667, 0.6667, 0.6667)
precision_recall_f1([0] * 99 + [1], [0] * 100)        → (0.0, 0.0, 0.0)     99% accuracy, useless
precision_recall_f1([1, 1, 0], [1, 0, 0], positive=0) → (0.5, 1.0, 0.6667)  F1 depends on which class is "positive"
macro_f1(["a", "b", "c", "a"], ["a", "b", "b", "a"])  → 0.5556             (1 + 0.6667 + 0) / 3
```

## Constraints

- Pure Python, no imports needed.
- Lists hold up to 100 000 labels; each function is O(n + k²) for k labels.
- Floats within `1e-12` of the exact fractions.

## Hints

1. Walking the two lists once, which cell of the matrix does each (truth, prediction) pair add one to? How do you find a label's row index without a linear search every time?
2. With one class marked positive, where in the confusion matrix do TP, FP and FN live?
3. A model predicts negative for every row. What is TP + FP, and what should precision be so that the metric still tells the truth?
4. For macro F1, which set of labels do you loop over, and what does each label contribute regardless of how many rows it has?

## Explain-back

- A fraud model scores 99% accuracy where 1% of transactions are fraud. What would its recall be if it predicted "not fraud" for everything, and why is accuracy the wrong metric here?
- Someone quotes "F1 = 0.8" with no positive class named. Why is that ambiguous? Show it with the `positive=0` example.
- How does moving the decision threshold trade precision against recall without retraining the model?
- Macro and micro averaging differ on imbalanced multiclass data. Which one lets a rare class drag the score down, and when do you want that?
