# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
import struct


def to_fp16(x: float) -> tuple[float, str]:
    try:
        value = struct.unpack("<e", struct.pack("<e", x))[0]
    except (OverflowError, struct.error):
        return math.copysign(math.inf, x), "overflow"
    if value == 0.0 and x != 0.0:
        return value, "underflow"
    return value, "ok"


def loss_scale_ok(grads: list[float], scale: float) -> bool:
    if scale <= 0:
        raise ValueError("scale must be positive")
    return all(to_fp16(g * scale)[1] == "ok" for g in grads)
