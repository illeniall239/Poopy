# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from bisect import bisect_right


def one_hot(values: list[str], vocabulary: list[str]) -> list[list[int]]:
    position = {category: i for i, category in enumerate(vocabulary)}
    if len(position) != len(vocabulary):
        raise ValueError("vocabulary contains a duplicate")
    unknown = len(vocabulary)
    rows = []
    for value in values:
        row = [0] * (unknown + 1)
        row[position.get(value, unknown)] = 1
        rows.append(row)
    return rows


def bucketize(x: float, boundaries: list[float]) -> int:
    if not boundaries:
        raise ValueError("boundaries must not be empty")
    if any(a >= b for a, b in zip(boundaries, boundaries[1:])):
        raise ValueError("boundaries must be strictly increasing")
    return bisect_right(boundaries, x)
