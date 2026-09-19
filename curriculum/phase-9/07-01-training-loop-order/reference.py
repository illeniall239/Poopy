# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Any, Callable

KEYS = ("zero_grad", "forward", "loss", "backward", "step")


def training_loop(step_fns: dict[str, Callable[..., Any]], batches: list[tuple[Any, Any]], epochs: int) -> list[float]:
    if epochs < 0:
        raise ValueError("epochs must be >= 0")
    if not batches:
        raise ValueError("batches must not be empty")
    missing = [k for k in KEYS if k not in step_fns]
    if missing:
        raise ValueError(f"step_fns is missing {missing}")

    history = []
    for _ in range(epochs):
        total = 0.0
        for x, y in batches:
            step_fns["zero_grad"]()
            out = step_fns["forward"](x)
            loss = step_fns["loss"](out, y)
            step_fns["backward"](loss)
            step_fns["step"]()
            total += float(loss)
        history.append(total / len(batches))
    return history
