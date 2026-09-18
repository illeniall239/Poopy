# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import bisect
import itertools
import random


def sample_categorical(probs: list[float], n: int, rng: random.Random) -> list[int]:
    if not probs or any(p < 0 for p in probs) or abs(sum(probs) - 1.0) > 1e-9:
        raise ValueError("probs must be non-empty, non-negative and sum to 1")
    if n < 0:
        raise ValueError("n must be non-negative")
    cumulative = list(itertools.accumulate(probs))
    last = len(probs) - 1
    return [min(bisect.bisect_right(cumulative, rng.random()), last) for _ in range(n)]


def empirical_frequencies(draws: list[int], k: int) -> list[float]:
    counts = [0] * k
    for d in draws:
        counts[d] += 1
    total = len(draws)
    return [c / total if total else 0.0 for c in counts]
