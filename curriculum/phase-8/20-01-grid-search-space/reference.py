# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from itertools import product


def grid(space: dict[str, list]) -> list[dict]:
    for name, values in space.items():
        if not isinstance(values, (list, tuple)) or not values:
            raise ValueError(f"{name!r} needs a non-empty list of values")
    names = sorted(space)
    return [dict(zip(names, combo)) for combo in product(*(space[n] for n in names))]
