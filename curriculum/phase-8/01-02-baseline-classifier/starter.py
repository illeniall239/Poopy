import random


def accuracy(y_true: list, y_pred: list) -> float:
    """Fraction of positions where y_true and y_pred agree; ValueError on empty or mismatched lengths."""
    raise NotImplementedError


def majority_class(train_labels: list):
    """Most frequent training label, ties to the first seen; ValueError if empty."""
    raise NotImplementedError


def majority_baseline_accuracy(train_labels: list, val_labels: list) -> float:
    """Accuracy on val_labels of always predicting the training majority class."""
    raise NotImplementedError


def random_baseline_accuracy(train_labels: list, val_labels: list, seed: int) -> float:
    """Accuracy on val_labels of seeded random draws with the training class frequencies."""
    raise NotImplementedError
