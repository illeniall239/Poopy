# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import math


def dot(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("length mismatch")
    return float(sum(x * y for x, y in zip(a, b)))


def norm(v: list[float], p: int = 2) -> float:
    if p == 1:
        return float(sum(abs(x) for x in v))
    if p == 2:
        return math.sqrt(dot(v, v))
    raise ValueError("p must be 1 or 2")


def cosine_similarity(a: list[float], b: list[float]) -> float:
    na, nb = norm(a), norm(b)
    if na == 0 or nb == 0:
        raise ValueError("cosine similarity is undefined for a zero vector")
    return dot(a, b) / (na * nb)
