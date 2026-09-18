# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def pearson(x: list[float], y: list[float]) -> float:
    if len(x) != len(y):
        raise ValueError("length mismatch")
    if len(x) < 2:
        raise ValueError("need at least two points")
    mx, my = sum(x) / len(x), sum(y) / len(y)
    dx = [a - mx for a in x]
    dy = [b - my for b in y]
    denom = math.sqrt(sum(a * a for a in dx) * sum(b * b for b in dy))
    if denom == 0:
        raise ValueError("correlation undefined for a constant input")
    return sum(a * b for a, b in zip(dx, dy)) / denom


def rank(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j + 2) / 2  # positions are 1-based: (i+1 + j+1) / 2
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(x: list[float], y: list[float]) -> float:
    if len(x) != len(y):
        raise ValueError("length mismatch")
    return pearson(rank(x), rank(y))
