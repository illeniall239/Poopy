# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math

import numpy as np

CHARS = ".abcdefghijklmnopqrstuvwxyz"
INDEX = {ch: i for i, ch in enumerate(CHARS)}


def _bigrams(word: str) -> list[tuple[int, int]]:
    if any(ch not in INDEX or ch == "." for ch in word):
        raise ValueError(f"{word!r} must contain only a-z")
    ids = [0] + [INDEX[ch] for ch in word] + [0]
    return list(zip(ids, ids[1:]))


def bigram_counts(words: list[str]) -> np.ndarray:
    counts = np.zeros((27, 27), dtype=int)
    for word in words:
        for i, j in _bigrams(word):
            counts[i, j] += 1
    return counts


def bigram_probs(counts: np.ndarray, smoothing: float = 0.0) -> np.ndarray:
    if smoothing < 0:
        raise ValueError("smoothing must be non-negative")
    smoothed = counts + float(smoothing)
    totals = smoothed.sum(axis=1, keepdims=True)
    return np.divide(smoothed, totals, out=np.zeros((27, 27)), where=totals > 0)


def sample(probs: np.ndarray, rng: np.random.Generator, n: int) -> list[str]:
    words = []
    for _ in range(n):
        chars, ix = [], 0
        while True:
            ix = int(rng.choice(27, p=probs[ix]))
            if ix == 0:
                break
            chars.append(CHARS[ix])
        words.append("".join(chars))
    return words


def avg_nll(words: list[str], probs: np.ndarray) -> float:
    if not words:
        raise ValueError("need at least one word")
    pairs = [pair for word in words for pair in _bigrams(word)]
    p = np.array([probs[i, j] for i, j in pairs])
    if np.any(p == 0):
        return math.inf
    return float(-np.log(p).mean())
