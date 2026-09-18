# A/B test

Topic: 9. Inferential statistics and A/B testing
Difficulty: 3 of 3

## Problem

Write three functions in pure Python (no NumPy; `math` and `random` allowed):

- `two_proportion_ztest(successes_a: int, n_a: int, successes_b: int, n_b: int) -> tuple[float, float]` — the pooled two-proportion z-test. With `p̂ₐ = sₐ/nₐ`, `p̂ᵦ = sᵦ/nᵦ` and the pooled `p̂ = (sₐ + sᵦ)/(nₐ + nᵦ)`, the statistic is `z = (p̂ᵦ - p̂ₐ) / sqrt(p̂ (1 - p̂) (1/nₐ + 1/nᵦ))` and the two-sided p-value is `erfc(|z| / √2)` (from `math.erfc`). Return `(z, p_value)`. Raise `ValueError` if either `n` is 0 or a count is outside `0..n`; if the pooled `p̂` is 0 or 1 return `(0.0, 1.0)`.
- `permutation_test(a: list[float], b: list[float], n_permutations: int, rng: random.Random) -> float` — the two-sided p-value for the difference in means `mean(b) - mean(a)`: pool the values, shuffle with `rng.shuffle` `n_permutations` times, split into the original sizes, and count how often `|permuted difference| >= |observed difference|`. Return `(count + 1) / (n_permutations + 1)`.
- `bootstrap_diff_ci(a: list[float], b: list[float], n_bootstrap: int, rng: random.Random, alpha: float = 0.05) -> tuple[float, float]` — resample each group with replacement (`rng.choices`) `n_bootstrap` times, record `mean(b*) - mean(a*)`, and return the `alpha/2` and `1 - alpha/2` empirical quantiles: sort the differences and take the elements at indices `floor(q · (n_bootstrap - 1))`.

## Examples

```
two_proportion_ztest(200, 1000, 250, 1000)   → (2.6117..., 0.00901...)     B converts 25% vs 20%
two_proportion_ztest(200, 1000, 200, 1000)   → (0.0, 1.0)
two_proportion_ztest(0, 100, 0, 100)         → (0.0, 1.0)

rng = random.Random(0)
permutation_test([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 999, rng)          → close to 1.0
permutation_test([1, 2, 3, 4, 5], [11, 12, 13, 14, 15], 999, rng)     → 1/1000 or a few thousandths
bootstrap_diff_ci(a, b, 2000, rng)  → an interval around mean(b) - mean(a)
```

## Constraints

- Groups up to 5 000 values, up to 5 000 permutations or bootstrap samples; the test must run in a few seconds.
- `z` and `p` must match the formula within `1e-9`; the permutation p-value and bootstrap interval are checked with tolerances against known cases.
- Same `rng` seed, same answer.

## Hints

1. The normal CDF is `Φ(z) = erfc(-z/√2) / 2`. Why is the two-sided p-value `erfc(|z|/√2)` and not `1 - Φ(|z|)`?
2. Under the null hypothesis both groups come from the same distribution. Which operation on the pooled list produces one "world where the null is true"?
3. Why `(count + 1) / (n + 1)` rather than `count / n`? What p-value would `count / n` give when no permutation reaches the observed difference, and is that credible?
4. `rng.choices(a, k=len(a))` draws with replacement. What does resampling with replacement simulate, and why must each group be resampled separately?

## Explain-back

- `p = 0.009`. Complete the sentence correctly: "If A and B truly converted at the same rate, then ..." Why is "there is a 99.1% chance B is better" wrong?
- A team checks the test every morning and stops the first day p drops below 0.05. Why is the real false-positive rate above 5%?
- The permutation test and the z-test gave similar p-values here. When would you trust the permutation test more?
- Twenty metrics were tested; one has p = 0.03. What is the expected number of significant metrics if nothing changed, and what would you do about it?
