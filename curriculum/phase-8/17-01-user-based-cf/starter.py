def predict_rating(ratings: dict[str, dict[str, float]], user: str, item: str, k: int) -> float:
    """Predict user's rating of item from the k most cosine-similar users who rated it, with fallbacks."""
    raise NotImplementedError
