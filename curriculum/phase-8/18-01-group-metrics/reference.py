# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from collections import defaultdict


def group_metrics(y_true: list[int], y_pred: list[int], groups: list) -> dict:
    if not y_true or not (len(y_true) == len(y_pred) == len(groups)):
        raise ValueError("inputs must be non-empty and the same length")
    counts = defaultdict(lambda: {"tp": 0, "fp": 0, "tn": 0, "fn": 0})
    for t, p, g in zip(y_true, y_pred, groups):
        key = ("t" if t == p else "f") + ("p" if p == 1 else "n")
        counts[g][key] += 1

    result = {}
    for g, c in counts.items():
        n = c["tp"] + c["fp"] + c["tn"] + c["fn"]
        positives, negatives = c["tp"] + c["fn"], c["fp"] + c["tn"]
        result[g] = {
            "n": n,
            "selection_rate": (c["tp"] + c["fp"]) / n,
            "tpr": c["tp"] / positives if positives else None,
            "fpr": c["fp"] / negatives if negatives else None,
            "accuracy": (c["tp"] + c["tn"]) / n,
        }
    return result
