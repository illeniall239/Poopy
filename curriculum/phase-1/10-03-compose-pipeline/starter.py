from typing import Callable

Step = Callable[[float], float]


def pipeline(steps: list[Step]) -> Step:
    """Return one Step that runs the given steps left to right."""
    raise NotImplementedError


def when(predicate: Callable[[float], bool], step: Step) -> Step:
    """Return a Step that applies step only when predicate(n) is true, else returns n unchanged."""
    raise NotImplementedError
