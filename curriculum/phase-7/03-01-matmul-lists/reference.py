# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def transpose(a: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*a)]


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    if len(a[0]) != len(b):
        raise ValueError(f"cannot multiply {len(a)}x{len(a[0])} by {len(b)}x{len(b[0])}")
    cols = transpose(b)
    return [[float(sum(x * y for x, y in zip(row, col))) for col in cols] for row in a]
