def nearest_by_euclidean(query: list[float], vectors: list[list[float]]) -> int:
    """Index of the vector closest to query by Euclidean distance (smallest index on ties)."""
    raise NotImplementedError


def nearest_by_cosine(query: list[float], vectors: list[list[float]]) -> int:
    """Index of the vector with the largest cosine similarity to query (smallest index on ties)."""
    raise NotImplementedError
