# User-based collaborative filtering

Topic: 17. Recommender systems basics
Difficulty: 1 of 3

## Problem

A ratings matrix is mostly empty, so store it sparsely: `ratings[user][item] = rating`, a dict of dicts that holds only the ratings that exist. Write one pure-Python function:

`predict_rating(ratings: dict[str, dict[str, float]], user: str, item: str, k: int) -> float`

1. **Similarity.** The similarity of `user` and another user `v` is the cosine over their co-rated items only (items both have rated): `Σ r_u,i · r_v,i / (√Σ r_u,i² · √Σ r_v,i²)`, where all three sums run over the co-rated items. A missing rating is unknown, not zero, so it never enters any sum. Users with no co-rated items have no similarity and are skipped.
2. **Neighbours.** Candidates are the other users who rated `item`, have at least one co-rated item with `user`, and have a positive similarity. Keep the `k` most similar; on equal similarity, the user id that sorts first alphabetically wins.
3. **Prediction.** The similarity-weighted average of the neighbours' ratings of `item`: `Σ sim · r_v,item / Σ sim`.
4. **Fallbacks.** If there are no neighbours, return the mean of `user`'s own ratings. If `user` has no ratings (a new user, possibly absent from `ratings`), return the mean rating of `item` over everyone who rated it; if nobody rated it either, return the mean of all ratings in the matrix.

Raise `ValueError` if `k < 1` or the matrix holds no ratings at all.

## Examples

```
ratings = {
    "ann": {"a": 5, "b": 3, "c": 4},
    "bob": {"a": 4, "b": 2, "d": 2},
    "bea": {"a": 4, "b": 2, "d": 4},
    "cat": {"a": 1, "b": 5, "c": 1, "d": 5},
    "dan": {"c": 2, "d": 3},
}
predict_rating(ratings, "ann", "d", 1)   → 3.0     dan shares only "c", so his cosine is exactly 1.0
predict_rating(ratings, "ann", "d", 2)   → 3.4993  dan (1.0) and bea (0.99705); bea beats bob on the tie
predict_rating(ratings, "ann", "z", 3)   → 4.0     nobody rated "z": ann's own mean
predict_rating(ratings, "zed", "d", 3)   → 3.5     new user: the mean rating of "d"
predict_rating(ratings, "ann", "d", 0)   → ValueError
```

## Constraints

- Pure Python: `math` is allowed, numpy is not.
- Up to 2 000 users and 5 000 items, each user with at most a few hundred ratings. Do not build a dense matrix.
- Results within `1e-9`.

## Hints

1. For two users, which items can you actually compare them on, and what happens to their cosine if you fill the missing ratings with 0 instead?
2. Which users can possibly help predict `ann`'s rating of `d`, before you compute any similarity?
3. What is the cosine between two users who share exactly one item, whatever their ratings are? Should you trust it as much as one computed from twenty shared items?
4. For a user who has never rated anything, what is the most reasonable number you can still return, and what is the next one if that fails too?

## Explain-back

- Why is treating a missing rating as 0 wrong here? What would it say about a user who simply has not seen a film?
- `dan` got similarity 1.0 from a single shared item and dominated the `k = 1` prediction. How would you guard against that, and what does it cost?
- What does your function do for a brand-new user, and why is crashing the wrong answer for a product?
- Plain cosine on raw ratings ignores that some users rate everything high. What would you subtract first, and how does that change the similarity?
