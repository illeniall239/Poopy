# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import math


def _check(query: list[float], vectors: list[list[float]]) -> None:
    if not vectors:
        raise ValueError("no candidate vectors")
    if any(len(v) != len(query) for v in vectors):
        raise ValueError("length mismatch")


def nearest_by_euclidean(query: list[float], vectors: list[list[float]]) -> int:
    _check(query, vectors)
    best, best_d2 = 0, math.inf
    for i, v in enumerate(vectors):
        d2 = sum((x - y) ** 2 for x, y in zip(query, v))
        if d2 < best_d2:
            best, best_d2 = i, d2
    return best


def nearest_by_cosine(query: list[float], vectors: list[list[float]]) -> int:
    _check(query, vectors)
    qn = math.sqrt(sum(x * x for x in query))
    if qn == 0:
        raise ValueError("zero query vector")
    best, best_cos = 0, -math.inf
    for i, v in enumerate(vectors):
        vn = math.sqrt(sum(x * x for x in v))
        if vn == 0:
            raise ValueError("zero candidate vector")
        cos = sum(x * y for x, y in zip(query, v)) / (qn * vn)
        if cos > best_cos:
            best, best_cos = i, cos
    return best
