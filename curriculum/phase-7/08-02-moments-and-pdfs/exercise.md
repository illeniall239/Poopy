# Moments and densities

Topic: 8. Probability for ML
Difficulty: 2 of 3

## Problem

Write five functions in pure Python (no NumPy; `math` allowed):

- `mean(sample: list[float]) -> float` — the arithmetic mean. `ValueError` on an empty list.
- `variance(sample: list[float], ddof: int = 0) -> float` — the average squared deviation from the mean, divided by `n - ddof`. `ddof=0` is the population variance, `ddof=1` the unbiased sample variance. `ValueError` if `n - ddof <= 0`.
- `expectation(values: list[float], probs: list[float]) -> float` — `Σ vᵢ pᵢ` for a discrete distribution. `ValueError` if the lengths differ, any probability is negative, or the probabilities do not sum to 1 within `1e-9`.
- `gaussian_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float` — the normal density `exp(-(x-mu)² / (2σ²)) / (σ √(2π))`. `ValueError` if `sigma <= 0`.
- `bernoulli_pmf(k: int, p: float) -> float` — `p` for `k == 1`, `1 - p` for `k == 0`, `0.0` for any other integer. `ValueError` if `p` is outside `[0, 1]`.

## Examples

```
mean([1, 2, 3, 4])                 → 2.5
variance([1, 2, 3, 4])             → 1.25
variance([1, 2, 3, 4], ddof=1)     → 1.6666...
expectation([1, 2, 6], [0.5, 0.25, 0.25])  → 2.5    a die weighted to 1
gaussian_pdf(0.0)                  → 0.3989...      1/sqrt(2π)
gaussian_pdf(0.0, sigma=0.1)       → 3.989...       a density above 1
bernoulli_pmf(1, 0.3)              → 0.3
bernoulli_pmf(2, 0.3)              → 0.0
variance([5], ddof=1)              → ValueError
```

## Constraints

- Samples up to 100 000 values; single pass plus one pass for deviations is fine.
- Must match `numpy.mean`, `numpy.var(ddof=...)` and closed forms within `1e-9`.

## Hints

1. `variance` needs the mean first. Can you call your own `mean`? What is squared, the deviations or the values?
2. `ddof=1` divides by `n - 1`. For which `n` does that become division by zero, and what should happen before you divide?
3. In `expectation`, which two things must you check about `probs` before trusting the weighted sum? Why compare the sum with a tolerance rather than `== 1`?
4. `gaussian_pdf(0, sigma=0.1)` is almost 4. Which quantity must integrate to 1, the density or the density times a width?

## Explain-back

- "Variance is the average deviation from the mean." What is wrong with that sentence, and what is the average deviation actually equal to?
- Why does the unbiased sample variance divide by `n - 1`? What does using the sample mean instead of the true mean do to the squared deviations?
- A density value of 3.98 is not a probability. What *is* the probability that a `N(0, 0.1)` variable equals exactly 0, and how do you get a probability from a PDF?
- `expectation` with `values = [0, 1]` and `probs = [1-p, p]` is a Bernoulli mean. What is its variance in terms of `p`, and for which `p` is it largest?
