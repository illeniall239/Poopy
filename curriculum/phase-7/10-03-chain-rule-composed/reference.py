# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from collections.abc import Callable

Pair = tuple[Callable[[float], float], Callable[[float], float]]


def intermediates(chain: list[Pair], x: float) -> list[float]:
    values = [x]
    for f, _ in chain:
        values.append(f(values[-1]))
    return values


def compose(chain: list[Pair], x: float) -> float:
    return intermediates(chain, x)[-1]


def chain_derivative(chain: list[Pair], x: float) -> float:
    values = intermediates(chain, x)
    d = 1.0
    for (_, f_prime), v in zip(chain, values):
        d *= f_prime(v)
    return d
