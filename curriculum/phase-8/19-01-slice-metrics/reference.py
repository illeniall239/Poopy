# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def slice_metrics(y_true: list, y_pred: list, feature_values: list, metric) -> list[tuple]:
    if not y_true or not (len(y_true) == len(y_pred) == len(feature_values)):
        raise ValueError("inputs must be non-empty and the same length")
    slices: dict = {}  # dicts keep insertion order, i.e. first appearance
    for t, p, v in zip(y_true, y_pred, feature_values):
        ts, ps = slices.setdefault(v, ([], []))
        ts.append(t)
        ps.append(p)
    results = [(v, metric(ts, ps), len(ts)) for v, (ts, ps) in slices.items()]
    return sorted(results, key=lambda r: r[1])  # stable: ties keep first-appearance order


def worst_errors(y_true: list[int], scores: list[float], n: int) -> list[int]:
    if len(y_true) != len(scores):
        raise ValueError("y_true and scores must have the same length")
    if n < 0:
        raise ValueError("n must be non-negative")
    mistakes = [j for j, (t, s) in enumerate(zip(y_true, scores)) if (1 if s >= 0.5 else 0) != t]
    mistakes.sort(key=lambda j: (-abs(scores[j] - 0.5), j))
    return mistakes[:n]
