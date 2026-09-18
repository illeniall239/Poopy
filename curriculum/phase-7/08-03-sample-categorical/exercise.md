# Categorical sampler

Topic: 8. Probability for ML
Difficulty: 2 of 3

## Problem

Write two functions in pure Python (no NumPy; `random` allowed):

- `sample_categorical(probs: list[float], n: int, rng: random.Random) -> list[int]` — draw `n` independent category indices `0..k-1` where index `i` is chosen with probability `probs[i]`. Use exactly one call to `rng.random()` per draw and walk the cumulative probabilities. Raise `ValueError` if `probs` is empty, any entry is negative, or the entries do not sum to 1 within `1e-9`; raise `ValueError` if `n < 0`.
- `empirical_frequencies(draws: list[int], k: int) -> list[float]` — the fraction of `draws` equal to each index `0..k-1` (a list of `k` floats summing to 1; all zeros if `draws` is empty).

The same seed must give the same draws, and different seeds different draws.

## Examples

```
rng = random.Random(0)
draws = sample_categorical([0.2, 0.5, 0.3], 10_000, rng)
empirical_frequencies(draws, 3)   → about [0.2, 0.5, 0.3], each within 0.02

sample_categorical([1.0], 5, rng)          → [0, 0, 0, 0, 0]
sample_categorical([0.0, 1.0], 3, rng)     → [1, 1, 1]      a zero-probability category never appears
sample_categorical([0.5, 0.6], 3, rng)     → ValueError     sums to 1.1
empirical_frequencies([0, 1, 1, 2], 3)     → [0.25, 0.5, 0.25]
```

## Constraints

- Up to 10 000 draws over up to 1 000 categories; precompute the cumulative sums once, not per draw.
- Float noise: the last cumulative value may be `0.9999999999`, so a draw of `u = 0.99999999999` must still map to the last category.
- The test checks determinism by reseeding, and frequencies with a tolerance, never exact counts.

## Hints

1. Sketch the unit interval cut into pieces of length `probs[0]`, `probs[1]`, ... Where does a uniform `u` in `[0, 1)` land, and which index is that?
2. Which list lets you find the piece with a scan (or `bisect`) instead of adding the probabilities up again every draw?
3. If the cumulative sums end at `0.9999999999` and `u` exceeds it, what index does a naive scan return? How do you clamp it?
4. Is it possible for a category with probability `0.5` to appear exactly 5 000 times in 10 000 draws? Would you write a test that demands it?

## Explain-back

- A seeded sampler gave frequencies `[0.198, 0.507, 0.295]` for `[0.2, 0.5, 0.3]`. Is it broken? What does the law of large numbers promise, and at what rate does the error shrink?
- Why must every draw use the same `rng` object rather than `random.Random(0)` created inside the loop?
- The sampler picks a token from a softmax over a vocabulary. What does "temperature" do to `probs` before sampling, and what happens to the frequencies as it goes to 0?
- Softmax outputs `[0.2, 0.5, 0.3]`. Is the model saying the middle class happens 50% of the time for inputs like this one? What word describes when that claim is true?
