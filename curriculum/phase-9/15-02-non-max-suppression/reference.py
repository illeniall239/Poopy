# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def iou(box_a: list[float], box_b: list[float]) -> float:
    w = max(0.0, min(box_a[2], box_b[2]) - max(box_a[0], box_b[0]))
    h = max(0.0, min(box_a[3], box_b[3]) - max(box_a[1], box_b[1]))
    inter = w * h
    area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
    return inter / (area_a + area_b - inter)


def nms(boxes: list[list[float]], scores: list[float], iou_threshold: float, labels: list[int] | None = None) -> list[int]:
    if len(boxes) != len(scores) or (labels is not None and len(labels) != len(boxes)):
        raise ValueError("boxes, scores and labels must have the same length")
    if not 0 <= iou_threshold <= 1:
        raise ValueError("iou_threshold must be in [0, 1]")
    labels = labels if labels is not None else [0] * len(boxes)
    order = sorted(range(len(boxes)), key=lambda i: -scores[i])  # stable: ties keep index order
    kept: list[int] = []
    for i in order:
        if all(labels[k] != labels[i] or iou(boxes[k], boxes[i]) <= iou_threshold for k in kept):
            kept.append(i)
    return kept
