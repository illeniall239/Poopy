# Content-based recommender

Topic: 17. Recommender systems basics
Difficulty: 2 of 3

## Problem

A content-based recommender describes every item by a feature vector (genre flags, tags, price band) and builds a profile of each user from the items they liked. Write two pure-Python functions:

- `user_profile(item_features: dict[str, list[float]], liked: list[str]) -> list[float]` returns the element-wise mean of the feature vectors of the `liked` items. Raise `ValueError` if `liked` is empty or names an item that is not in `item_features`.
- `recommend(profile: list[float], item_features: dict[str, list[float]], n: int, exclude: set[str]) -> list[str]` ranks every item not in `exclude` by the cosine similarity between its vector and `profile`, highest first, and returns the ids of the top `n` (fewer if fewer items remain; `n = 0` gives `[]`). An item whose vector is all zeros has similarity 0. On equal similarity, the id that sorts first alphabetically comes first. Raise `ValueError` if `profile` is all zeros or `n < 0`.

Ranking is by cosine, not by dot product: an item with large feature values must not win only because its vector is long.

## Examples

```
feats = {"a": [1, 0, 0], "b": [0.9, 0.1, 0], "c": [0, 1, 0], "d": [0, 0, 1],
         "e": [1, 1, 0], "f": [1, 1, 0], "g": [0, 50, 1]}
user_profile(feats, ["a", "b"])                         → [0.95, 0.05, 0.0]
recommend([0.95, 0.05, 0.0], feats, 3, {"a", "b"})      → ["e", "f", "c"]   e and f tie (0.743); c (0.05256) just beats g (0.05255)
recommend([0.95, 0.05, 0.0], feats, 10, {"a", "b"})     → ["e", "f", "c", "g", "d"]
user_profile(feats, [])                                  → ValueError
```

## Constraints

- Pure Python: `math` is allowed, numpy is not.
- Up to 10 000 items with up to 100 features each.
- Profile values within `1e-9`.

## Hints

1. What does the mean of the liked items' vectors point toward, and what would a single liked item give you?
2. `g = [0, 50, 1]` and `c = [0, 1, 0]` point almost the same way. Should g score higher because its values are larger? Which measure says yes and which says no?
3. How can one sort key express "highest similarity first, then id ascending" without two sorts?
4. Which items must never come back, and what should happen to an item whose vector has length 0?

## Explain-back

- Item `h` was added this morning and nobody has rated it yet. Can this recommender show it? Could the user-based collaborative filter from the previous exercise?
- A new user has liked nothing. What can you recommend, and why is popularity the usual fallback?
- Why cosine and not the dot product here? What kind of item would the dot product keep pushing to the top?
- This recommender only suggests items like the ones already liked. What does that do to a user's feed over months, and how would you add variety?
