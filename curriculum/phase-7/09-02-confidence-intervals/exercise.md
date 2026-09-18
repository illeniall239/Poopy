# Confidence intervals

Topic: 9. Inferential statistics and A/B testing
Difficulty: 2 of 3

## Problem

Write three functions in pure Python (no NumPy; `math` allowed), all using the normal approximation with a caller-supplied critical value `z` (1.96 for 95%):

- `mean_ci(sample: list[float], z: float = 1.96) -> tuple[float, float]` — `x̄ ± z · s / √n` where `s` is the sample standard deviation with `ddof=1`. Raise `ValueError` if `n < 2`.
- `proportion_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float]` — `p̂ ± z · sqrt(p̂ (1 - p̂) / n)` with `p̂ = successes / n`, clipped to `[0, 1]`. Raise `ValueError` if `n <= 0` or `successes` is outside `0..n`.
- `sample_size_for_margin(margin: float, z: float = 1.96, p: float = 0.5) -> int` — the smallest integer `n` such that `z · sqrt(p (1 - p) / n) <= margin`; that is, `ceil(z² p (1 - p) / margin²)`. Raise `ValueError` if `margin <= 0` or `p` is outside `[0, 1]`.

Return tuples of `(low, high)` floats.

## Examples

```
mean_ci([2, 4, 4, 4, 5, 5, 7, 9])              → (3.4207..., 6.5793...)    mean 5, s = 2.138, n = 8
proportion_ci(50, 100)                         → (0.402, 0.598)
proportion_ci(0, 20)                           → (0.0, 0.0)
proportion_ci(100, 100, z=1.96)                → (1.0, 1.0)
sample_size_for_margin(0.03)                   → 1068       the classic "±3 points" poll
sample_size_for_margin(0.05, p=0.1)            → 139
mean_ci([1.0])                                 → ValueError
```

## Constraints

- Samples up to 100 000 values.
- Must match values computed with NumPy within `1e-9`; sample sizes must be exact integers.
- The interval must contain the point estimate and be symmetric around it before clipping.

## Hints

1. The standard error of a mean is `s / √n`. Which `s`, population or sample? What does `ddof=1` change in the formula?
2. For a proportion, the standard error uses `p̂ (1 - p̂)`. What happens to the width when `p̂` is `0` or `1`, and why does the interval collapse there?
3. `sample_size_for_margin` inverts `margin = z · sqrt(p(1-p)/n)`. Solve for `n` on paper before writing code. Why `ceil` rather than `round`?
4. Why is `p = 0.5` the default for planning? What is special about `p(1-p)` at `0.5`?

## Explain-back

- A 95% CI for the mean is `(3.42, 6.58)`. Does that mean 95% of the data lies in that range? What does the 95% refer to?
- Halving the margin of error multiplies the required sample size by what factor? Show it from the formula.
- `proportion_ci(0, 20)` returns `(0, 0)`. Is it credible that the true proportion is exactly 0? What assumption of the normal approximation broke?
- How does a confidence interval relate to a hypothesis test at the same level? If the 95% CI for a difference excludes 0, what can you say about the p-value?
