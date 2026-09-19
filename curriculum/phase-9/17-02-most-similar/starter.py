import numpy as np


def most_similar(word: str, table: np.ndarray, vocab: list[str], k: int) -> list[tuple[str, float]]:
    """Return up to k (word, cosine similarity) pairs, highest first, excluding the query word."""
    raise NotImplementedError
