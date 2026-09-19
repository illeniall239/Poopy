# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def _area(box: list[float]) -> float:
    if len(box) != 4 or box[2] <= box[0] or box[3] <= box[1]:
        raise ValueError(f"invalid box {box}")
    return (box[2] - box[0]) * (box[3] - box[1])


def iou(box_a: list[float], box_b: list[float]) -> float:
    area_a, area_b = _area(box_a), _area(box_b)
    w = max(0.0, min(box_a[2], box_b[2]) - max(box_a[0], box_b[0]))
    h = max(0.0, min(box_a[3], box_b[3]) - max(box_a[1], box_b[1]))
    inter = w * h
    return inter / (area_a + area_b - inter)
