# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def _check(y_true: list[int], scores: list[float]) -> tuple[int, int]:
    if not y_true or len(y_true) != len(scores):
        raise ValueError("y_true and scores must be non-empty and the same length")
    if any(y not in (0, 1) for y in y_true):
        raise ValueError("labels must be 0 or 1")
    n_pos = sum(y_true)
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0:
        raise ValueError("AUC needs at least one positive and one negative")
    return n_pos, n_neg


def roc_auc(y_true: list[int], scores: list[float]) -> float:
    n_pos, n_neg = _check(y_true, scores)
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        average_rank = (i + j) / 2 + 1  # positions i..j hold ranks i+1..j+1
        for k in range(i, j + 1):
            ranks[order[k]] = average_rank
        i = j + 1
    rank_sum = sum(r for r, y in zip(ranks, y_true) if y == 1)
    return (rank_sum - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def roc_curve(y_true: list[int], scores: list[float]) -> tuple[list[float], list[float]]:
    n_pos, n_neg = _check(y_true, scores)
    pairs = sorted(zip(scores, y_true), key=lambda p: -p[0])
    fpr, tpr = [0.0], [0.0]
    tp = fp = 0
    for i, (score, label) in enumerate(pairs):
        tp += label
        fp += 1 - label
        is_last_of_run = i + 1 == len(pairs) or pairs[i + 1][0] != score
        if is_last_of_run:
            fpr.append(fp / n_neg)
            tpr.append(tp / n_pos)
    return fpr, tpr


def auc_trapezoid(fpr: list[float], tpr: list[float]) -> float:
    return sum((fpr[i + 1] - fpr[i]) * (tpr[i + 1] + tpr[i]) / 2 for i in range(len(fpr) - 1))
