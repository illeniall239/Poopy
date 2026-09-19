# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import random
from collections import Counter


def accuracy(y_true: list, y_pred: list) -> float:
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be non-empty and the same length")
    return sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)


def majority_class(train_labels: list):
    if not train_labels:
        raise ValueError("no training labels")
    # Counter keeps first-seen order, and most_common keeps that order among ties.
    return Counter(train_labels).most_common(1)[0][0]


def majority_baseline_accuracy(train_labels: list, val_labels: list) -> float:
    prediction = majority_class(train_labels)
    return accuracy(val_labels, [prediction] * len(val_labels))


def random_baseline_accuracy(train_labels: list, val_labels: list, seed: int) -> float:
    if not train_labels:
        raise ValueError("no training labels")
    counts = Counter(train_labels)
    classes = list(counts)
    predictions = random.Random(seed).choices(classes, weights=[counts[c] for c in classes], k=len(val_labels))
    return accuracy(val_labels, predictions)
