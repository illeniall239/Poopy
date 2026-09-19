# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def pr_curve(y_true: list[int], scores: list[float]) -> list[tuple[float, float, float]]:
    if not y_true or len(y_true) != len(scores):
        raise ValueError("y_true and scores must be non-empty and the same length")
    if any(y not in (0, 1) for y in y_true):
        raise ValueError("labels must be 0 or 1")
    n_pos = sum(y_true)
    if n_pos == 0:
        raise ValueError("recall is undefined without positive labels")
    pairs = sorted(zip(scores, y_true), key=lambda p: -p[0])
    points = []
    tp = fp = 0
    for i, (score, label) in enumerate(pairs):
        tp += label
        fp += 1 - label
        if i + 1 == len(pairs) or pairs[i + 1][0] != score:
            points.append((score, tp / (tp + fp), tp / n_pos))
    return points


def _f1(precision: float, recall: float) -> float:
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def best_threshold(
    y_true: list[int], scores: list[float], metric: str = "f1", min_precision: float | None = None
) -> float:
    if metric == "f1":
        candidates = [(t, _f1(p, r)) for t, p, r in pr_curve(y_true, scores)]
    elif metric == "precision_floor":
        if min_precision is None or not 0 < min_precision <= 1:
            raise ValueError("precision_floor needs min_precision in (0, 1]")
        candidates = [(t, r) for t, p, r in pr_curve(y_true, scores) if p >= min_precision]
        if not candidates:
            raise ValueError("no threshold reaches the precision floor")
    else:
        raise ValueError(f"unknown metric: {metric!r}")
    # Candidates are in descending threshold order; max() keeps the first of equal values,
    # which is the highest threshold.
    return max(candidates, key=lambda c: c[1])[0]
