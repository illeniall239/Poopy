def user_profile(item_features: dict[str, list[float]], liked: list[str]) -> list[float]:
    """Element-wise mean of the liked items' feature vectors; ValueError if empty or unknown."""
    raise NotImplementedError


def recommend(profile: list[float], item_features: dict[str, list[float]], n: int, exclude: set[str]) -> list[str]:
    """Top n item ids not in exclude by cosine similarity to profile, ties by id."""
    raise NotImplementedError
