import numpy as np


def bigram_counts(words: list[str]) -> np.ndarray:
    """Return the (27, 27) count matrix of next-token pairs, with "." (index 0) as start and end."""
    raise NotImplementedError


def bigram_probs(counts: np.ndarray, smoothing: float = 0.0) -> np.ndarray:
    """Return row-normalized (counts + smoothing); rows summing to 0 stay all zeros."""
    raise NotImplementedError


def sample(probs: np.ndarray, rng: np.random.Generator, n: int) -> list[str]:
    """Generate n words, drawing each token with one rng.choice(27, p=probs[current])."""
    raise NotImplementedError


def avg_nll(words: list[str], probs: np.ndarray) -> float:
    """Return the mean negative log-likelihood per bigram (math.inf if any bigram has p = 0)."""
    raise NotImplementedError
