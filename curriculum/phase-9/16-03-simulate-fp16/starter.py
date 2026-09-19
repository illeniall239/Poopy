def to_fp16(x: float) -> tuple[float, str]:
    """Round x to float16 with struct; return (value, "ok" | "overflow" | "underflow")."""
    raise NotImplementedError


def loss_scale_ok(grads: list[float], scale: float) -> bool:
    """Return True if every grad * scale converts to float16 with status "ok"."""
    raise NotImplementedError
