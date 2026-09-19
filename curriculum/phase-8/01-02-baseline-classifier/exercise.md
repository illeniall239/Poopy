# Baseline classifier

Topic: 1. Framing a problem, baselines, and when not to use ML
Difficulty: 1 of 3

## Problem

A classifier's accuracy means nothing until you know what a model with no features scores. Write four pure-Python functions (no numpy). Labels may be any hashable values (strings, ints).

- `accuracy(y_true: list, y_pred: list) -> float` returns the fraction of positions where the two lists agree. Raise `ValueError` if the lengths differ or the lists are empty.
- `majority_class(train_labels: list)` returns the most frequent label in `train_labels`. On a tie, return the tied label that appears first in `train_labels`. Raise `ValueError` on an empty list.
- `majority_baseline_accuracy(train_labels: list, val_labels: list) -> float` fits the majority class on `train_labels` only and returns its accuracy on `val_labels` (predicting that class for every validation row).
- `random_baseline_accuracy(train_labels: list, val_labels: list, seed: int) -> float` predicts every validation row by drawing a label at random with the training class frequencies, and returns the accuracy of those draws on `val_labels`. Draw exactly like this so the result is reproducible: `classes` are the distinct training labels in first-seen order, `counts` their training counts, and the predictions are `random.Random(seed).choices(classes, weights=counts, k=len(val_labels))`. Raise `ValueError` if `train_labels` is empty.

The validation labels must never influence either baseline's predictions.

## Examples

```
accuracy(["a", "b", "a"], ["a", "a", "a"])                 → 0.6666...
majority_class(["cat", "dog", "dog"])                      → "dog"
majority_class([1, 0, 0, 1])                               → 1        tie: 1 is seen first
majority_baseline_accuracy([0, 0, 0, 1], [0, 1, 0, 0])     → 0.75
random_baseline_accuracy(train, val, 0)                    → about 0.82 when both are 90% class 0 (0.9² + 0.1²)
```

## Constraints

- Pure Python: `random`, `collections` and `math` are allowed, numpy is not.
- Lists hold at most 100 000 labels.
- Every function is O(n + m).

## Hints

1. If you had to give the same answer for every row without looking at it, which answer would be right most often, and which data are you allowed to learn that from?
2. `collections.Counter` counts labels. In what order does it report labels that have the same count, and does that match the tie rule?
3. A random guesser that picks class `c` with probability `p_c`, on rows whose true class is `c` with probability `q_c`: what is the chance a single guess is right?
4. Why must the class frequencies for the random baseline come from the training labels, and what would it mean if they came from `val_labels`?

## Explain-back

- A fraud model scores 92% accuracy. Why is that number meaningless until you know the majority-class rate, and what would you compare it to?
- With 90% of rows in one class, which scores higher: the majority baseline or the frequency-random baseline? Why is "beats random" not a success criterion?
- Why can the majority baseline's accuracy on validation data differ from its accuracy on training data, even though it has no features?
- Accuracy hides which class the errors fall on. Which metric would expose that the majority baseline never finds a single fraud case?
