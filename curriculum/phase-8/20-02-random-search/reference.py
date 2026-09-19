# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
import random


def _check(name: str, spec) -> None:
    if isinstance(spec, list):
        if not spec:
            raise ValueError(f"{name!r}: empty list of choices")
        return
    if not (isinstance(spec, tuple) and len(spec) == 3 and spec[0] in ("uniform", "loguniform")):
        raise ValueError(f"{name!r}: expected a list or (kind, low, high)")
    kind, low, high = spec
    if not low < high:
        raise ValueError(f"{name!r}: low must be below high")
    if kind == "loguniform" and low <= 0:
        raise ValueError(f"{name!r}: a log-uniform range must be positive")


def _sample(spec, rng: random.Random):
    if isinstance(spec, list):
        return rng.choice(spec)
    kind, low, high = spec
    if kind == "uniform":
        return rng.uniform(low, high)
    return math.exp(rng.uniform(math.log(low), math.log(high)))


def random_search(space: dict, n: int, rng: random.Random) -> list[dict]:
    if n < 0:
        raise ValueError("n must be non-negative")
    for name, spec in space.items():
        _check(name, spec)
    names = sorted(space)
    return [{name: _sample(space[name], rng) for name in names} for _ in range(n)]
