# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def mean_iou(pred_mask: list[list[int]], true_mask: list[list[int]], n_classes: int) -> tuple[list[float | None], float]:
    if n_classes < 1:
        raise ValueError("n_classes must be at least 1")
    if not pred_mask or len(pred_mask) != len(true_mask) or any(len(p) != len(t) for p, t in zip(pred_mask, true_mask)):
        raise ValueError("masks must be non-empty and the same shape")
    inter = [0] * n_classes
    union = [0] * n_classes
    for p_row, t_row in zip(pred_mask, true_mask):
        for p, t in zip(p_row, t_row):
            if not (0 <= p < n_classes and 0 <= t < n_classes):
                raise ValueError(f"class id out of range: {p}, {t}")
            if p == t:
                inter[p] += 1
                union[p] += 1
            else:
                union[p] += 1
                union[t] += 1
    per_class = [i / u if u else None for i, u in zip(inter, union)]
    present = [v for v in per_class if v is not None]
    if not present:
        raise ValueError("masks are empty")
    return per_class, sum(present) / len(present)
