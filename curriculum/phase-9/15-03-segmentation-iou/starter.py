def mean_iou(pred_mask: list[list[int]], true_mask: list[list[int]], n_classes: int) -> tuple[list[float | None], float]:
    """Return (per-class IoU with None for classes absent from both masks, mean over the rest)."""
    raise NotImplementedError
