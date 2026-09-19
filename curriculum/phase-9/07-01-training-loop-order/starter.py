from typing import Any, Callable


def training_loop(step_fns: dict[str, Callable[..., Any]], batches: list[tuple[Any, Any]], epochs: int) -> list[float]:
    """Run zero_grad, forward, loss, backward, step for every batch; return each epoch's mean loss."""
    raise NotImplementedError
