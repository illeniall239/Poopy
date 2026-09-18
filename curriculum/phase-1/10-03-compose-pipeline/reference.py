# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from functools import reduce
from typing import Callable

Step = Callable[[float], float]


def pipeline(steps: list[Step]) -> Step:
    fixed_steps = list(steps)
    return lambda n: reduce(lambda value, step: step(value), fixed_steps, n)


def when(predicate: Callable[[float], bool], step: Step) -> Step:
    return lambda n: step(n) if predicate(n) else n
