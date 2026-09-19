def iou(box_a: list[float], box_b: list[float]) -> float:
    """Return intersection area / union area of two [x1, y1, x2, y2] boxes."""
    raise NotImplementedError


def nms(boxes: list[list[float]], scores: list[float], iou_threshold: float, labels: list[int] | None = None) -> list[int]:
    """Return indices of boxes kept by (per-class, if labels given) NMS, highest score first."""
    raise NotImplementedError
