# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
import random
from typing import Any


def _check(name: str, spec: tuple) -> None:
    kind = spec[0]
    if kind == "log":
        _, low, high = spec
        if not 0 < low < high:
            raise ValueError(f"{name}: log range needs 0 < low < high")
    elif kind == "uniform":
        _, low, high = spec
        if not low < high:
            raise ValueError(f"{name}: uniform range needs low < high")
    elif kind == "choice":
        if not spec[1]:
            raise ValueError(f"{name}: choice needs at least one option")
    else:
        raise ValueError(f"{name}: unknown spec kind {kind!r}")


def _draw(spec: tuple, rng: random.Random) -> Any:
    kind = spec[0]
    if kind == "log":
        return math.exp(rng.uniform(math.log(spec[1]), math.log(spec[2])))
    if kind == "uniform":
        return rng.uniform(spec[1], spec[2])
    return rng.choice(spec[1])


def sample_configs(space: dict[str, tuple], n: int, rng: random.Random) -> list[dict[str, Any]]:
    if n < 0:
        raise ValueError("n must be non-negative")
    for name, spec in space.items():
        _check(name, spec)
    return [{name: _draw(spec, rng) for name, spec in space.items()} for _ in range(n)]
